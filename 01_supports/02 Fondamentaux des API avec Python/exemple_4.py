from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API pour mon super escape game!"}

PLAYERS = [
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
    {
        "id": 42,
        "name": "Zelda",
        "score": 3000,
        "level": 99,
    }
]


@app.get("/players")
def get_players():
    return PLAYERS


@app.get("/players/{player_id}")
def get_player(player_id: int):
    for player in PLAYERS:
        if player["id"] == player_id:
            return player

    # Si la boucle se termine sans rien trouver :
    return {"error": "Player not found"}


from pydantic import BaseModel

class Player(BaseModel):
    name: str
    score: int
    level: int

@app.post("/players")
def create_player(player: Player):
    # 1. On transforme l'objet validé par Pydantic en dictionnaire
    new_player = player.model_dump()
    
    # 2. On génère un nouvel ID (par exemple, la taille de la liste + 1)
    new_player["id"] = len(PLAYERS) + 1
    
    # 3. On l'ajoute à notre fausse base de données
    PLAYERS.append(new_player)
    
    return new_player



# Lancer le serveur depuis le terminal :
# fastapi dev exemple_4.py
# tester http://127.0.0.1:8000/players
# tester http://127.0.0.1:8000/players/1
# tester http://127.0.0.1:8000/players/99
