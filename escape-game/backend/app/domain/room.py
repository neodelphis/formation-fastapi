"""Room — Salle du jeu, conteneur d'Items, Doors et Puzzles.

Une salle représente un lieu physique du scénario (ex: "Salle des Serveurs",
"Antichambre du Mainframe"). Elle agrège :
  * des :class:`Item` que le joueur peut examiner ou ramasser,
  * des :class:`Door` qui mènent vers d'autres salles,
  * des :class:`Puzzle` que le joueur peut tenter de résoudre.

Cette classe illustre le principe de composition en POO : une Room *contient*
d'autres objets du domaine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from app.domain.door import Door
from app.domain.game_element import GameElement
from app.domain.item import Item
from app.domain.puzzle import Puzzle


@dataclass
class Room(GameElement):
    """Salle du jeu.

    Attributes:
        items: Liste des objets présents dans la salle.
        doors: Liste des portes de la salle.
        puzzles: Liste des énigmes de la salle.
        is_start: True si c'est la salle de départ du joueur.
        is_exit: True si c'est la salle de sortie (condition de victoire).
    """

    items: List[Item] = field(default_factory=list)
    doors: List[Door] = field(default_factory=list)
    puzzles: List[Puzzle] = field(default_factory=list)
    is_start: bool = False
    is_exit: bool = False

    def find_item(self, item_id: str) -> Optional[Item]:
        """Recherche un item par son identifiant."""
        return next((i for i in self.items if i.id == item_id), None)

    def find_door(self, door_id: str) -> Optional[Door]:
        """Recherche une porte par son identifiant."""
        return next((d for d in self.doors if d.id == door_id), None)

    def find_puzzle(self, puzzle_id: str) -> Optional[Puzzle]:
        """Recherche un puzzle par son identifiant."""
        return next((p for p in self.puzzles if p.id == puzzle_id), None)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update(
            {
                "items": [i.to_dict() for i in self.items],
                "doors": [d.to_dict() for d in self.doors],
                "puzzles": [p.to_dict() for p in self.puzzles],
                "is_start": self.is_start,
                "is_exit": self.is_exit,
            }
        )
        return data
