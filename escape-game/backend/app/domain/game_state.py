"""GameState — État global mutable du jeu (singleton en mémoire).

Le `GameState` orchestre l'ensemble des entités du domaine :
  * les salles du scénario,
  * les joueurs connectés,
  * l'inventaire de chaque joueur,
  * l'état de verrouillage des portes (qui peut changer en cours de partie).

C'est ici que vit la logique applicative : résolution d'un puzzle, ramassage
d'un item, déplacement du joueur entre les salles, etc.

En production, cet état serait persisté en base de données ; ici, pour la
version Alpha pédagogique, il vit en mémoire (volatile au redémarrage).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.domain.door import Door
from app.domain.player import Player
from app.domain.room import Room


@dataclass
class GameSubmissionResult:
    """Résultat d'une soumission de puzzle."""

    success: bool
    message: str
    unlocked_door_id: Optional[str] = None
    reward_item_ids: List[str] = field(default_factory=list)


class GameState:
    """État global du jeu, en mémoire.

    Le `GameState` est instancié une seule fois (singleton) et partagé
    entre toutes les requêtes HTTP via l'injection de dépendances FastAPI.
    """

    def __init__(self) -> None:
        self._rooms: Dict[str, Room] = {}
        self._players: Dict[str, Player] = {}
        self._puzzle_to_door: Dict[str, str] = {}
        self._puzzle_to_rewards: Dict[str, List[str]] = {}

    # ------------------------------------------------------------------ #
    # Scénario : enregistrement des salles et mapping puzzle -> porte
    # ------------------------------------------------------------------ #
    def register_room(self, room: Room) -> None:
        self._rooms[room.id] = room

    def link_puzzle_to_door(self, puzzle_id: str, door_id: str) -> None:
        """Associe la résolution d'un puzzle au déverrouillage d'une porte."""
        self._puzzle_to_door[puzzle_id] = door_id

    def link_puzzle_to_rewards(self, puzzle_id: str, item_ids: List[str]) -> None:
        """Associe la résolution d'un puzzle à l'obtention d'items de récompense."""
        self._puzzle_to_rewards[puzzle_id] = item_ids

    # ------------------------------------------------------------------ #
    # Joueurs
    # ------------------------------------------------------------------ #
    def add_player(self, player: Player) -> Player:
        self._players[player.id] = player
        return player

    def get_player(self, player_id: str) -> Optional[Player]:
        return self._players.get(player_id)

    def list_players(self) -> List[Player]:
        return list(self._players.values())

    def remove_player(self, player_id: str) -> bool:
        return self._players.pop(player_id, None) is not None

    # ------------------------------------------------------------------ #
    # Salles
    # ------------------------------------------------------------------ #
    def list_rooms(self) -> List[Room]:
        return list(self._rooms.values())

    def get_room(self, room_id: str) -> Optional[Room]:
        return self._rooms.get(room_id)

    # ------------------------------------------------------------------ #
    # Logique applicative : puzzle + déplacement
    # ------------------------------------------------------------------ #
    def submit_puzzle(
        self, player_id: str, puzzle_id: str, attempt_code: str
    ) -> GameSubmissionResult:
        """Tente de résoudre un puzzle pour le compte d'un joueur.

        Recherche le puzzle dans toutes les salles (un puzzle appartient à une
        salle), vérifie la réponse via le polymorphisme de `check_solution`,
        puis applique les effets de bord (déverrouillage de porte, items de
        récompense) en cas de succès.
        """
        player = self.get_player(player_id)
        if player is None:
            return GameSubmissionResult(
                success=False, message=f"Joueur inconnu : {player_id}"
            )

        puzzle = None
        for room in self._rooms.values():
            p = room.find_puzzle(puzzle_id)
            if p is not None:
                puzzle = p
                break

        if puzzle is None:
            return GameSubmissionResult(
                success=False, message=f"Puzzle introuvable : {puzzle_id}"
            )

        # Délégation polymorphe : CodePuzzle et HashPuzzle ont chacun leur
        # implémentation de check_solution.
        if not puzzle.check_solution(attempt_code):
            return GameSubmissionResult(
                success=False,
                message="Code incorrect. L'IA Sentinel vous observe...",
            )

        player.solve(puzzle_id)

        # Effets de bord : déverrouillage de porte + récompenses.
        unlocked_door_id: Optional[str] = None
        door_id = self._puzzle_to_door.get(puzzle_id)
        if door_id is not None:
            for room in self._rooms.values():
                door = room.find_door(door_id)
                if door is not None:
                    door.unlock()
                    unlocked_door_id = door.id
                    break

        reward_item_ids: List[str] = []
        rewards = self._puzzle_to_rewards.get(puzzle_id, [])
        for item_id in rewards:
            player.add_item(item_id)
            reward_item_ids.append(item_id)

        message = puzzle.reward_message
        if unlocked_door_id is not None:
            message += " Porte déverrouillée !"
        if reward_item_ids:
            message += f" Items obtenus : {', '.join(reward_item_ids)}."

        return GameSubmissionResult(
            success=True,
            message=message,
            unlocked_door_id=unlocked_door_id,
            reward_item_ids=reward_item_ids,
        )

    def move_player(self, player_id: str, room_id: str) -> Optional[Player]:
        """Déplace un joueur vers une salle (si elle existe)."""
        player = self.get_player(player_id)
        room = self.get_room(room_id)
        if player is None or room is None:
            return None
        player.visit(room_id)
        return player

    def pickup_item(self, player_id: str, item_id: str) -> Optional[Player]:
        """Ajoute un item à l'inventaire du joueur s'il est dans sa salle courante."""
        player = self.get_player(player_id)
        if player is None or player.current_room_id is None:
            return None
        room = self.get_room(player.current_room_id)
        if room is None:
            return None
        item = room.find_item(item_id)
        if item is None:
            return None
        player.add_item(item_id)
        return player

    # ------------------------------------------------------------------ #
    # Reset (utile pour les tests et la réinitialisation du scénario)
    # ------------------------------------------------------------------ #
    def reset(self) -> None:
        self._rooms.clear()
        self._players.clear()
        self._puzzle_to_door.clear()
        self._puzzle_to_rewards.clear()
