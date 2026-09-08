# Fondamentaux des API avec Python

## FastAPI · Pydantic

---

# Objectifs

À la fin de cette séance, vous serez capables de :

* comprendre ce qu'est une API ;
* expliquer le fonctionnement d'une communication client / serveur ;
* comprendre les principes fondamentaux d'une API REST ;
* utiliser les principales méthodes HTTP ;
* créer une API REST avec **FastAPI** ;
* définir des routes et leurs paramètres ;
* recevoir et retourner des données JSON ;
* créer des modèles avec **Pydantic** ;
* valider automatiquement les données reçues ;
* définir le contrat de réponse d'une API ;
* comprendre le rôle d'**OpenAPI** ;
* utiliser **Swagger UI** pour tester une API ;
* comprendre comment FastAPI génère automatiquement sa documentation.

---

# 16. Les Type Hints

Nous voulons que `player_id` soit un entier.

Nous écrivons :

```python
@app.get("/players/{player_id}")
def get_player(player_id: int):
    return {
        "id": player_id
    }
```

Maintenant :

```text
/player/42
```

est valide.

Mais :

```text
/players/hello
```

ne l'est pas.

FastAPI connaît le type attendu grâce au **Type Hint** :

```python
player_id: int
```

---

# 17. Les Type Hints deviennent un outil de validation

C'est une caractéristique importante de FastAPI.

Dans Python :

```python
player_id: int
```

est normalement une annotation de type.

FastAPI utilise cette information pour :

* **analyser la requête** ;
* **convertir les données** ;
* **valider les données** ;
* **générer la documentation**.


```mermaid
flowchart TD
    A[Type Hint] --> B{FastAPI}
    B --> C[Validation]
    B --> D[Docs]
    B --> E[Conversion]

    %% Styles
    classDef client_data fill:#2B5E83,stroke:#fff,stroke-width:2px,color:#fff
    classDef process_api fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000
    classDef result_db fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px,color:#000

    class A client_data
    class B process_api
    class C,D,E result_db
````

---

# 18. Où sont les joueurs ?

Pour le moment, nous allons utiliser une simple liste Python.

```python
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
```

Notre route :

```python
@app.get("/players")
def get_players():
    return players
```

---

# 19. Récupérer un joueur

Nous pouvons rechercher le joueur dans notre liste :

```python
@app.get("/players/{player_id}")
def get_player(player_id: int):
    for player in players:
        if player["id"] == player_id:
            return player

    return {"error": "Player not found"}
```

Nous pouvons maintenant appeler :

```text
GET /players/1
```

ou :

```text
GET /players/2
```

---

# 20. Un problème apparaît...

Notre API doit également permettre de **créer** un joueur.

Nous voulons recevoir :

```json
{
    "name": "Charlie",
    "score": 1000,
    "level": 1
}
```

Mais comment indiquer à FastAPI :

* quels champs sont obligatoires ?
* quels sont leurs types ?
* quelles valeurs sont acceptées ?
* à quoi doit ressembler le JSON ?

C'est ici que **Pydantic** intervient.

---

# 21. Pydantic

Pydantic permet de définir des modèles de données Python.

Nous créons une classe :

```python
from pydantic import BaseModel


class Player(BaseModel):
    name: str
    score: int
    level: int
```

Nous venons de définir le modèle d'un joueur.

---

# 22. Le modèle comme contrat

Notre modèle signifie :

```text
Player
│
├── name  → string
├── score → integer
└── level → integer
```

On peut donc considérer `Player` comme un **contrat de données**.

```text
JSON reçu
    │
    ▼
┌──────────────┐
│   Pydantic   │
│    Player    │
└──────┬───────┘
       │
       ▼
Données validées
```

---

# 23. Utiliser un modèle dans une route

Nous pouvons maintenant écrire :

```python
@app.post("/players")
def create_player(player: Player):
    return player
```

Le Type Hint :

```python
player: Player
```

indique à FastAPI :

> Le corps de la requête doit respecter le modèle `Player`.

---

# 24. Tester avec JSON

Une requête `POST` peut contenir :

```json
{
    "name": "Charlie",
    "score": 1000,
    "level": 1
}
```

FastAPI :

1. reçoit le JSON ;
2. demande à Pydantic de le valider ;
3. construit un objet `Player` ;
4. appelle notre fonction.

```text
JSON
 │
 ▼
FastAPI
 │
 ▼
Pydantic
 │
 ├── valide
 │
 ▼
Player
 │
 ▼
create_player()
```

---

# 25. Et si les données sont incorrectes ?

Essayons :

```json
{
    "name": "Charlie",
    "score": "hello",
    "level": 1
}
```

Le champ `score` doit être un entier.

FastAPI détecte automatiquement le problème.

Nous n'avons pas écrit :

```python
if not isinstance(score, int):
    ...
```

La validation est réalisée automatiquement.

---

# 26. Ajouter des contraintes

Les types ne sont pas toujours suffisants.

Par exemple :

> Le score ne peut pas être négatif.

Nous pouvons utiliser `Field`.

```python
from pydantic import BaseModel, Field


class Player(BaseModel):
    name: str = Field(min_length=3)
    score: int = Field(ge=0)
    level: int = Field(ge=1)
```

Nous exprimons maintenant des règles métier simples :

```text
name  → au moins 3 caractères
score → >= 0
level → >= 1
```

---

# 27. Pourquoi est-ce intéressant ?

Nous avons défini les règles **une seule fois**.

```python
class Player(BaseModel):
    name: str = Field(min_length=3)
    score: int = Field(ge=0)
    level: int = Field(ge=1)
```

FastAPI/Pydantic peuvent ensuite utiliser ces informations pour :

* valider les données ;
* générer des erreurs ;
* construire le schéma OpenAPI ;
* documenter automatiquement l'API.

```text
               Player
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
   Validation   OpenAPI   Documentation
```

---

# 28. Repenser notre API

Nous avons maintenant :

```text
GET    /players
GET    /players/{player_id}

POST   /players

PUT    /players/{player_id}

DELETE /players/{player_id}
```

Nous avons donc les principaux éléments d'une API REST.

```text
              Game API
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
    Routing    Models     Validation
       │          │          │
       └──────────┼──────────┘
                  ▼
               HTTP/JSON
```

---

# 29. Le contrat d'une API

Une API doit permettre au client de savoir :

> « Comment dois-je communiquer avec le serveur ? »

Par exemple :

```text
POST /players

Request body:

{
    "name": "Charlie",
    "score": 1000,
    "level": 1
}
```

Le client doit savoir :

* que la route existe ;
* qu'elle utilise `POST` ;
* quels champs envoyer ;
* quels sont leurs types ;
* quels champs sont obligatoires ;
* quelle réponse attendre ;
* quelles erreurs peuvent être retournées.

Tout cela constitue une partie du **contrat de l'API**.

---