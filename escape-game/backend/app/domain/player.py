"""Player — Joueur participant à l'Escape Game.

Un joueur possède un inventaire d'items ramassés au cours de la partie
et un suivi de son avancement (salles visitées, puzzles résolus).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from app.domain.game_element import GameElement


@dataclass
class Player(GameElement):
    """Joueur de l'Escape Game.

    Attributes:
        inventory: Liste des IDs des items ramassés par le joueur.
        visited_rooms: Liste des IDs des salles visitées.
        solved_puzzles: Liste des IDs des puzzles résolus.
        current_room_id: Salle où se trouve actuellement le joueur.
    """

    inventory: List[str] = field(default_factory=list)
    visited_rooms: List[str] = field(default_factory=list)
    solved_puzzles: List[str] = field(default_factory=list)
    current_room_id: Optional[str] = None

    def add_item(self, item_id: str) -> None:
        """Ajoute un item à l'inventaire s'il n'y est pas déjà."""
        if item_id not in self.inventory:
            self.inventory.append(item_id)

    def has_item(self, item_id: str) -> bool:
        return item_id in self.inventory

    def visit(self, room_id: str) -> None:
        """Marque une salle comme visitée."""
        if room_id not in self.visited_rooms:
            self.visited_rooms.append(room_id)
        self.current_room_id = room_id

    def solve(self, puzzle_id: str) -> None:
        """Marque un puzzle comme résolu."""
        if puzzle_id not in self.solved_puzzles:
            self.solved_puzzles.append(puzzle_id)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update(
            {
                "inventory": list(self.inventory),
                "visited_rooms": list(self.visited_rooms),
                "solved_puzzles": list(self.solved_puzzles),
                "current_room_id": self.current_room_id,
            }
        )
        return data
