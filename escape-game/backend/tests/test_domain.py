"""Tests unitaires du domaine POO — pytest.

Exécuter avec :
    cd backend
    pytest -v
"""

import hashlib

from app.domain.door import Door
from app.domain.item import Item
from app.domain.puzzle import CodePuzzle, HashPuzzle
from app.domain.room import Room
from app.domain.player import Player
from app.domain.game_state import GameState


# ---------------------------------------------------------------------- #
# GameElement / Item / Door
# ---------------------------------------------------------------------- #
def test_item_to_dict_contains_type():
    item = Item(id="i1", name="Clé", description="Une clé rouillée.", usable=True)
    d = item.to_dict()
    assert d["id"] == "i1"
    assert d["name"] == "Clé"
    assert d["usable"] is True
    assert d["type"] == "item"


def test_door_unlock_mutates_state():
    door = Door(id="d1", name="Porte", description="", is_locked=True)
    assert door.is_locked is True
    door.unlock()
    assert door.is_locked is False


# ---------------------------------------------------------------------- #
# CodePuzzle
# ---------------------------------------------------------------------- #
def test_code_puzzle_correct_answer():
    p = CodePuzzle(id="p1", name="Code", description="", secret_code="1234")
    assert p.check_solution("1234") is True


def test_code_puzzle_wrong_answer():
    p = CodePuzzle(id="p1", name="Code", description="", secret_code="1234")
    assert p.check_solution("0000") is False


# ---------------------------------------------------------------------- #
# HashPuzzle
# ---------------------------------------------------------------------- #
def test_hash_puzzle_correct_answer():
    # Hash SHA-256 de "password"
    expected = hashlib.sha256(b"password").hexdigest()
    p = HashPuzzle(
        id="p2", name="Hash", description="", expected_hash=expected
    )
    assert p.check_solution("password") is True


def test_hash_puzzle_wrong_answer():
    expected = hashlib.sha256(b"password").hexdigest()
    p = HashPuzzle(
        id="p2", name="Hash", description="", expected_hash=expected
    )
    assert p.check_solution("wrong") is False


def test_hash_puzzle_from_plaintext_factory():
    p = HashPuzzle.from_plaintext(
        id="p3", name="Hash", description="", plaintext="neon2099"
    )
    assert p.check_solution("neon2099") is True
    assert p.check_solution("Neon2099") is False  # sensible à la casse


def test_hash_puzzle_does_not_expose_solution_in_to_dict():
    p = HashPuzzle.from_plaintext(
        id="p4", name="Hash", description="", plaintext="secret"
    )
    d = p.to_dict()
    assert "expected_hash" not in d
    assert "secret" not in str(d)
    assert d["solution_exposed"] is False


# ---------------------------------------------------------------------- #
# Room
# ---------------------------------------------------------------------- #
def test_room_find_helpers():
    item = Item(id="i1", name="Clé", description="")
    door = Door(id="d1", name="Porte", description="")
    puzzle = CodePuzzle(id="p1", name="Code", description="", secret_code="1")
    room = Room(
        id="r1", name="Salle", description="", items=[item], doors=[door], puzzles=[puzzle]
    )
    assert room.find_item("i1") is item
    assert room.find_door("d1") is door
    assert room.find_puzzle("p1") is puzzle
    assert room.find_item("nope") is None


# ---------------------------------------------------------------------- #
# GameState — submit_puzzle polymorphe
# ---------------------------------------------------------------------- #
def test_game_state_submit_code_puzzle_unlocks_door():
    state = GameState()
    door = Door(id="d1", name="Porte", description="", is_locked=True, target_room_id="r2")
    puzzle = CodePuzzle(id="p1", name="Code", description="", secret_code="1234")
    room = Room(id="r1", name="Salle", description="", doors=[door], puzzles=[puzzle])
    state.register_room(room)
    state.link_puzzle_to_door("p1", "d1")

    player = Player(id="player-x", name="X", description="")
    state.add_player(player)

    result = state.submit_puzzle("player-x", "p1", "1234")
    assert result.success is True
    assert door.is_locked is False
    assert result.unlocked_door_id == "d1"
    assert "p1" in player.solved_puzzles


def test_game_state_submit_hash_puzzle():
    state = GameState()
    puzzle = HashPuzzle.from_plaintext(
        id="p2", name="Hash", description="", plaintext="neon2099"
    )
    room = Room(id="r1", name="Salle", description="", puzzles=[puzzle])
    state.register_room(room)

    player = Player(id="player-y", name="Y", description="")
    state.add_player(player)

    assert state.submit_puzzle("player-y", "p2", "neon2099").success is True
    assert state.submit_puzzle("player-y", "p2", "wrong").success is False


def test_game_state_submit_unknown_player():
    state = GameState()
    result = state.submit_puzzle("ghost", "any", "any")
    assert result.success is False
    assert "Joueur inconnu" in result.message


# ---------------------------------------------------------------------- #
# Player
# ---------------------------------------------------------------------- #
def test_player_inventory_dedup():
    p = Player(id="player-1", name="A", description="")
    p.add_item("key")
    p.add_item("key")
    assert p.inventory == ["key"]


def test_player_visit_tracks_history():
    p = Player(id="player-1", name="A", description="")
    p.visit("room-1")
    p.visit("room-1")
    p.visit("room-2")
    assert p.visited_rooms == ["room-1", "room-2"]
    assert p.current_room_id == "room-2"
