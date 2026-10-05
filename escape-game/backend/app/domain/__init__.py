"""Domaine métier — Modélisation POO de l'Escape Game.

Ce package contient les classes métier pures, sans dépendance à FastAPI ou Pydantic.
La séparation domaine / API permet de tester la logique métier indépendamment.
"""

from app.domain.game_element import GameElement
from app.domain.item import Item
from app.domain.door import Door
from app.domain.puzzle import Puzzle, CodePuzzle, HashPuzzle
from app.domain.room import Room
from app.domain.player import Player
from app.domain.game_state import GameState

__all__ = [
    "GameElement",
    "Item",
    "Door",
    "Puzzle",
    "CodePuzzle",
    "HashPuzzle",
    "Room",
    "Player",
    "GameState",
]
