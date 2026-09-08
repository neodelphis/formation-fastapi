from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API pour mon super escape game!"}

players = [
    {
        "id": 1,
        "name": "Alice",
        "score": 1200,
        "level": 12,
    },
    {
        "id": 2,
        "name": "Bob",
        "score": 950,
        "level": 9,
    },
]

@app.get("/players")
def get_players():
    return players


@app.get("/players/{player_id}")
def get_player(player_id: int):
    for player in players:
        if player["id"] == player_id:
            return player

    return {"error": "Player not found"}


# Lancer le serveur depuis le terminal :
# fastapi dev exemple_4.py