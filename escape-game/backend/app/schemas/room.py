"""Schémas Pydantic pour les salles."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ItemOut(BaseModel):
    id: str
    name: str
    description: str
    type: str
    usable: bool = False


class DoorOut(BaseModel):
    id: str
    name: str
    description: str
    type: str
    is_locked: bool
    required_item_id: str | None = None
    target_room_id: str | None = None


class PuzzleOut(BaseModel):
    """Représentation publique d'un puzzle (jamais la solution)."""

    id: str
    name: str
    description: str
    type: str
    reward_message: str
    puzzle_kind: str | None = None
    hash_algorithm: str | None = None
    solution_exposed: bool = False


class RoomOut(BaseModel):
    id: str
    name: str
    description: str
    type: str
    items: list[ItemOut] = Field(default_factory=list)
    doors: list[DoorOut] = Field(default_factory=list)
    puzzles: list[PuzzleOut] = Field(default_factory=list)
    is_start: bool = False
    is_exit: bool = False


class RoomSummary(BaseModel):
    """Résumé d'une salle pour la liste (sans le détail des items)."""

    id: str
    name: str
    description: str
    is_start: bool = False
    is_exit: bool = False
    items_count: int = 0
    puzzles_count: int = 0
