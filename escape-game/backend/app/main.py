"""Point d'entrée FastAPI — Application principale.

Lance l'application avec :
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Documentation interactive :
    http://127.0.0.1:8000/docs        (Swagger UI)
    http://127.0.0.1:8000/redoc       (ReDoc)
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, player_game, players
from app.services.game_engine import ENGINE_VERSION, GAME_TITLE

app = FastAPI(
    title=f"DigitalEscape Studio — {GAME_TITLE}",
    description=(
        "Moteur backend du jeu d'Escape Game interactif.\n\n"
        "**Thème** : Operation: Neon Cyberpunk\n\n"
        "Le joueur doit infiltrer un mainframe contrôlé par l'IA Sentinel, "
        "résoudre des puzzles (codes en clair et hashes SHA-256) et déclencher "
        "l'auto-destruction du système.\n\n"
        "Toutes les routes sont auto-documentées via Swagger UI (`/docs`)."
    ),
    version=ENGINE_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS : autorise le frontend Vite (dev) et le frontend nginx (prod) à appeler l'API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://localhost:4173",   # Vite preview
        "http://localhost:8080",   # Frontend nginx (docker-compose)
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routers
app.include_router(health.router)
app.include_router(players.router)
app.include_router(player_game.router)


@app.get("/")
def root() -> dict:
    """Racine de l'API — redirige vers /docs pour la documentation."""
    return {
        "message": f"Bienvenue dans {GAME_TITLE} !",
        "docs": "/docs",
        "health": "/health",
    }
