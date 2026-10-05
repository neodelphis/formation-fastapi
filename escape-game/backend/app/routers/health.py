"""Router de santé et métadonnées du moteur."""

from __future__ import annotations

from fastapi import APIRouter

from app.services.game_engine import ENGINE_VERSION, GAME_TITLE, GAME_MASTER

router = APIRouter(tags=["meta"])


@router.get("/health")
def health() -> dict:
    """Endpoint de contrôle de santé du service.

    Retourne le statut du moteur, le titre du jeu et la version.
    Utilisé par Docker / les orchestrateurs pour les healthchecks.
    """
    return {
        "status": "online",
        "game_title": GAME_TITLE,
        "game_master": GAME_MASTER,
        "engine_version": ENGINE_VERSION,
    }
