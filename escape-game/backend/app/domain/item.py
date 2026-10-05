"""Item — Objet interactif que le joueur peut ramasser ou examiner.

Hérite de `GameElement`. Un Item est un objet purement descriptif : une clé,
un parchemin, un terminal informatique, un badge d'accès, etc. La logique
d'interaction (déverrouillage de porte, déclenchement de puzzle) est portée
par les classes `Door` et `Puzzle`.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.game_element import GameElement


@dataclass
class Item(GameElement):
    """Objet interactif du jeu.

    Attributes:
        usable: Indique si l'item peut être utilisé (ex: une clé) ou seulement
            examiné (ex: une note informative).
    """

    usable: bool = False

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["usable"] = self.usable
        return data
