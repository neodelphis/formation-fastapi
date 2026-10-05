"""Tests d'intégration de l'API FastAPI via TestClient.

Exécuter avec :
    cd backend
    pytest -v
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "online"
    assert body["game_title"] == "Operation: Neon Cyberpunk"
    assert body["engine_version"] == "1.0.0"


def test_list_rooms():
    r = client.get("/rooms")
    assert r.status_code == 200
    rooms = r.json()
    assert len(rooms) == 3
    ids = {room["id"] for room in rooms}
    assert ids == {"server-room", "security-hub", "mainframe-core"}


def test_get_room_detail():
    r = client.get("/rooms/security-hub")
    assert r.status_code == 200
    room = r.json()
    assert room["id"] == "security-hub"
    assert len(room["puzzles"]) == 1
    puzzle = room["puzzles"][0]
    # On ne doit JAMAIS exposer le hash ni la solution via l'API.
    assert "expected_hash" not in puzzle
    assert puzzle["solution_exposed"] is False


def test_get_unknown_room_returns_404():
    r = client.get("/rooms/does-not-exist")
    assert r.status_code == 404


def test_list_players_has_default_player():
    r = client.get("/players")
    assert r.status_code == 200
    players = r.json()
    ids = {p["id"] for p in players}
    assert "player-1" in ids


def test_create_player():
    r = client.post(
        "/players",
        json={"id": "player-test", "name": "Testeur", "description": "Test"},
    )
    assert r.status_code == 201
    assert r.json()["id"] == "player-test"


def test_create_duplicate_player_returns_409():
    r = client.post(
        "/players",
        json={"id": "player-1", "name": "Dup", "description": ""},
    )
    assert r.status_code == 409


def test_delete_player():
    client.post(
        "/players",
        json={"id": "player-del", "name": "ToDelete", "description": ""},
    )
    r = client.delete("/players/player-del")
    assert r.status_code == 204


def test_submit_puzzle_success():
    r = client.post(
        "/puzzles/submit",
        json={
            "puzzle_id": "puzzle-hub-password",
            "attempt_code": "neon2099",
            "player_id": "player-1",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    assert body["unlocked_door_id"] == "door-core"


def test_submit_puzzle_wrong_code():
    r = client.post(
        "/puzzles/submit",
        json={
            "puzzle_id": "puzzle-hub-password",
            "attempt_code": "wrong-password",
            "player_id": "player-1",
        },
    )
    assert r.status_code == 200
    assert r.json()["success"] is False


def test_submit_puzzle_empty_code_returns_422():
    """Cas clé du TP : un code vide doit déclencher un 422 Pydantic."""
    r = client.post(
        "/puzzles/submit",
        json={
            "puzzle_id": "puzzle-hub-password",
            "attempt_code": "   ",
            "player_id": "player-1",
        },
    )
    assert r.status_code == 422


def test_submit_puzzle_unknown_player_returns_404():
    r = client.post(
        "/puzzles/submit",
        json={
            "puzzle_id": "puzzle-hub-password",
            "attempt_code": "neon2099",
            "player_id": "ghost-player",
        },
    )
    assert r.status_code == 404
