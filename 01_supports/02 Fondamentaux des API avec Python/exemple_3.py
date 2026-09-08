from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API pour mon super escape game!"}

PLAYERS = {
    "1": {"id": 1, "name": "Alice", "score": 1200},
    "2": {"id": 2, "name": "Bob", "score": 950},
    "42": {"id": 42, "name": "Zelda", "score": 3000}
}

@app.get("/players")
def get_players():
    # On retourne la liste de tous les joueurs
    return list(PLAYERS.values())

@app.get("/players/{player_id}")
def get_player(player_id):
    # Par défaut, player_id est du texte (str)
    return PLAYERS.get(player_id)

# Lancer le serveur depuis le terminal :
# fastapi dev exemple_3.py
# tester http://127.0.0.1:8000/players
# tester http://127.0.0.1:8000/players/42
