from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

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

    return {"error": "Player not found"}


# Définition du contrat de données avec les contraintes métier
class Player(BaseModel):
    name: str = Field(min_length=3, max_length=99)
    score: int = Field(ge=0, le=99999)
    level: int = Field(ge=1, le=99)

@app.post("/players")
def create_player(player: Player):
    # 1. On transforme l'objet validé par Pydantic en dictionnaire
    new_player = player.model_dump()
    
    # 2. On génère un nouvel ID (par exemple, la taille de la liste + 1)
    new_player["id"] = len(PLAYERS) + 1
    
    # 3. On l'ajoute à notre fausse base de données
    PLAYERS.append(new_player)
    
    return new_player

@app.put("/players/{player_id}")
def update_player(player_id: int, player: Player):
    for index, existing_player in enumerate(PLAYERS):
        if existing_player["id"] == player_id:
            updated_player = player.model_dump()
            updated_player["id"] = player_id
            PLAYERS[index] = updated_player
            return updated_player

    raise HTTPException(status_code=404, detail="Player not found")

@app.delete("/players/{player_id}")
def delete_player(player_id: int):
    for index, player in enumerate(PLAYERS):
        if player["id"] == player_id:
            deleted_player = PLAYERS.pop(index)
            return {
                "message": "Player deleted",
                "player": deleted_player,
            }

    raise HTTPException(status_code=404, detail="Player not found")

# Lancer le serveur depuis le terminal :
# fastapi dev exemple_6.py

# Exemples de tests avec curl (serveur lancé sur http://127.0.0.1:8000)
#
# Consulter tous les joueurs :
# curl http://127.0.0.1:8000/players
#
# Consulter un joueur :
# curl http://127.0.0.1:8000/players/1
#
# Créer un joueur :
# curl -X POST http://127.0.0.1:8000/players \
#   -H "Content-Type: application/json" \
#   -d '{"name":"Link","score":1800,"level":20}'
#
# Remplacer complètement le joueur 1 :
# curl -X PUT http://127.0.0.1:8000/players/1 \
#   -H "Content-Type: application/json" \
#   -d '{"name":"Alice Updated","score":1500,"level":15}'
#
# Supprimer le joueur 1 :
# curl -X DELETE http://127.0.0.1:8000/players/1
#
# Tester les erreurs, par exemple pour un joueur inexistant :
# curl -i http://127.0.0.1:8000/players/999
# A vous de créer d'autres tests pour les autres routes et les cas d'erreur!