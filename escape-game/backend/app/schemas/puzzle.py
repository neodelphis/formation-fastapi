"""Schémas Pydantic pour les puzzles et soumissions."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class PuzzleSubmission(BaseModel):
    """Payload de soumission d'une tentative de puzzle (POST /puzzles/submit)."""

    puzzle_id: str = Field(
        ...,
        min_length=1,
        description="Identifiant unique du puzzle à résoudre.",
        examples=["puzzle-hub-password"],
    )
    attempt_code: str = Field(
        ...,
        description="Tentative du joueur (texte, code ou mot de passe).",
        examples=["neon2099"],
    )
    player_id: str = Field(
        ...,
        min_length=1,
        description="Identifiant du joueur qui soumet la tentative.",
        examples=["player-1"],
    )

    @field_validator("attempt_code")
    @classmethod
    def code_must_not_be_empty(cls, v: str) -> str:
        # Le code soumis ne peut pas être vide ni composé uniquement
        # d'espaces : Pydantic lèvera une ValueError → 422 Unprocessable Entity.
        if v is None or not v.strip():
            raise ValueError("Le code soumis ne peut pas être vide.")
        return v

    @field_validator("puzzle_id", "player_id")
    @classmethod
    def ids_must_not_be_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("L'identifiant ne peut pas être vide.")
        return v.strip()


class PuzzleSubmissionResult(BaseModel):
    """Résultat d'une soumission de puzzle."""

    success: bool
    message: str
    unlocked_door_id: str | None = None
    reward_item_ids: list[str] = Field(default_factory=list)
