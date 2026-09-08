from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API pour mon super escape game!"}


# Lancer le serveur depuis le terminal :
# fastapi dev exemple_2.py