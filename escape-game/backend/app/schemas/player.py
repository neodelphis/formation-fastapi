"""Schémas Pydantic pour les joueurs."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class PlayerCreate(BaseModel):
    """Payload de création d'un joueur (POST /players)."""

    id: str = Field(
        ...,
        min_length=3,
        max_length=40,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Identifiant unique (3-40 caractères alphanumériques, _ ou -).",
        examples=["player-2"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Pseudonyme affichable du joueur.",
        examples=["Hack3rGhost"],
    )
    description: str = Field(
        default="",
        max_length=500,
        description="Courte bio du personnage (optionnelle).",
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Le nom ne peut pas être vide.")
        return v.strip()


class PlayerOut(BaseModel):
    """Représentation sortante d'un joueur."""

    id: str
    name: str
    description: str
    type: str
    inventory: list[str] = Field(default_factory=list)
    visited_rooms: list[str] = Field(default_factory=list)
    solved_puzzles: list[str] = Field(default_factory=list)
    current_room_id: str | None = None
