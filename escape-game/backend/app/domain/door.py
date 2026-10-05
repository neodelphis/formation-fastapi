"""Door — Porte reliant deux salles, éventuellement verrouillée.

Une porte peut être :
  * Ouverte (`is_locked=False`) : le joueur peut passer librement.
  * Verrouillée (`is_locked=True`) : elle nécessite un `required_item_id`
    spécifique pour être déverrouillée, OU être déverrouillée via la
    résolution d'un puzzle associé.

Le verrouillage est géré côté `GameState` (état mutable du jeu), mais
l'attribut `is_locked` est aussi porté par la porte pour refléter l'état
initial défini par le Game Master dans le scénario.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.domain.game_element import GameElement


@dataclass
class Door(GameElement):
    """Porte du jeu, potentiellement verrouillée.

    Attributes:
        is_locked: True si la porte est verrouillée à l'initialisation.
        required_item_id: Identifiant de l'Item qui déverrouille la porte.
            None si la porte s'ouvre via un puzzle ou est libre d'accès.
        target_room_id: Identifiant de la salle vers laquelle mène la porte.
    """

    is_locked: bool = False
    required_item_id: Optional[str] = None
    target_room_id: Optional[str] = None

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update(
            {
                "is_locked": self.is_locked,
                "required_item_id": self.required_item_id,
                "target_room_id": self.target_room_id,
            }
        )
        return data

    def unlock(self) -> None:
        """Déverrouille la porte (mutation d'état)."""
        self.is_locked = False
