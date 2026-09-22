import logging

from fastapi import FastAPI

from app.routers.players import router as players_router


logging.basicConfig(level=logging.INFO)


app = FastAPI(
    title='Game API',
    description='API de démonstration pour un escape game',
    version='1.0.0',
)


app.include_router(players_router)


@app.get('/')
def home() -> dict:
    return {
        'message': 'Bienvenue sur l API pour mon super escape game!'
    }