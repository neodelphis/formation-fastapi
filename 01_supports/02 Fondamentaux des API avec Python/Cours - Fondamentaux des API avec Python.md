



# 30. Le problème de la documentation

Imaginez une API avec :

```text
50 endpoints
```

Comment documenter tout cela ?

On pourrait écrire un document à la main :

```text
GET /players

Description :
Récupère la liste des joueurs.

Paramètres :
...

Réponse :
...
```

Mais cela présente un problème :

> Le code et la documentation peuvent finir par ne plus correspondre.

FastAPI propose une autre approche.

---

# 31. OpenAPI

**OpenAPI** est une spécification permettant de décrire une API.

Elle permet notamment de décrire :

* les routes ;
* les méthodes HTTP ;
* les paramètres ;
* les modèles ;
* les données d'entrée ;
* les données de sortie ;
* les réponses possibles.

FastAPI génère automatiquement cette description.

---

# 32. OpenAPI JSON

Notre serveur expose automatiquement :

```text
/openapi.json
```

Par exemple :

```text
http://127.0.0.1:8000/openapi.json
```

Nous obtenons un document JSON décrivant notre API.

Il contient notamment :

```text
paths
components
schemas
parameters
responses
...
```

Ce document constitue le **contrat machine-readable** de notre API.

---

# 33. De FastAPI à OpenAPI

Voici le mécanisme fondamental à retenir :

```text
                 Code Python
                     │
                     │
              Type Hints
                     │
                     ▼
                  FastAPI
                     │
                     │
                Pydantic
                     │
                     ▼
                OpenAPI JSON
                     │
              ┌──────┴──────┐
              ▼             ▼
        Swagger UI         ReDoc
          /docs            /redoc
```

---

# 34. Swagger UI

FastAPI génère automatiquement une interface interactive :

```text
/docs
```

Par exemple :

```text
http://127.0.0.1:8000/docs
```

Cette interface est appelée :

> **Swagger UI**

Elle permet de :

* voir les endpoints ;
* voir les paramètres ;
* voir les modèles ;
* tester les requêtes ;
* observer les réponses.

---

# 35. Tester une API avec Swagger

Dans Swagger UI :

```text
GET /players
```

Puis :

> Try it out

et :

> Execute

Swagger envoie réellement la requête à notre serveur.

Nous obtenons par exemple :

```text
Request URL:
http://127.0.0.1:8000/players

Response code:
200
```

Puis :

```json
[
    {
        "id": 1,
        "name": "Alice",
        "score": 1200,
        "level": 12
    }
]
```

---

# 36. Swagger n'est pas l'API

Attention à une distinction importante.

```text
                 API
                  │
                  │ décrite par
                  ▼
               OpenAPI
                  │
          ┌───────┴───────┐
          ▼               ▼
     Swagger UI          ReDoc
```

**OpenAPI** décrit l'API.

**Swagger UI** est une interface permettant de visualiser et tester cette description.

---

# 37. ReDoc

FastAPI fournit également une autre interface :

```text
/redoc
```

Par exemple :

```text
http://127.0.0.1:8000/redoc
```

Nous avons donc :

| URL             | Rôle            |
| --------------- | --------------- |
| `/docs`         | Swagger UI      |
| `/redoc`        | ReDoc           |
| `/openapi.json` | Contrat OpenAPI |

---

# 38. Pourquoi cette génération automatique est intéressante ?

Nous avons écrit :

```python
class Player(BaseModel):
    name: str = Field(min_length=3)
    score: int = Field(ge=0)
    level: int = Field(ge=1)
```

Et :

```python
@app.post("/players")
def create_player(player: Player):
    return player
```

FastAPI peut en déduire :

```text
POST /players

Body:
Player

name  → string, minimum 3 caractères
score → integer, minimum 0
level → integer, minimum 1
```

Nous n'avons pas écrit cette documentation manuellement.

---

# 39. Le rôle des Type Hints

C'est probablement l'une des idées les plus importantes de FastAPI.

Dans FastAPI, les Type Hints ne servent pas uniquement à rendre le code plus lisible.

Ils permettent au framework de comprendre notre API.

Exemple :

```python
@app.get("/players/{player_id}")
def get_player(player_id: int):
    ...
```

FastAPI comprend :

```text
player_id
    │
    └── integer
```

Et :

```python
def create_player(player: Player):
```

lui indique :

```text
request body
     │
     ▼
Player
```

---

# 40. Entrées et sorties

Une API possède deux directions de données.

```text
                 API
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
     Request             Response
        │                   │
        ▼                   ▼
     Pydantic             Pydantic
```

Pour les données reçues :

```python
def create_player(player: Player):
```

Pour les données retournées :

```python
def get_player(...) -> Player:
```

ou explicitement :

```python
@app.get(
    "/players/{player_id}",
    response_model=Player
)
def get_player(player_id: int):
    ...
```

---

# 41. Pourquoi définir un modèle de réponse ?

Le modèle de réponse permet de définir ce que l'API doit retourner.

Par exemple :

```python
class Player(BaseModel):
    id: int
    name: str
    score: int
    level: int
```

Puis :

```python
@app.get("/players/{player_id}", response_model=Player)
def get_player(player_id: int):
    ...
```

Nous avons maintenant un contrat explicite :

```text
GET /players/{player_id}

Response:

{
    "id": integer,
    "name": string,
    "score": integer,
    "level": integer
}
```

---

# 42. Un modèle pour la création, un autre pour la réponse

Dans une véritable application, nous ne voulons pas forcément utiliser le même modèle partout.

Par exemple :

```python
class PlayerCreate(BaseModel):
    name: str
    score: int
    level: int
```

Et :

```python
class Player(BaseModel):
    id: int
    name: str
    score: int
    level: int
```

Pourquoi ?

Parce que l'`id` est généré par le serveur.

Le client ne doit donc pas nécessairement l'envoyer.

```text
Client                       Server

name ──────────────────────►
score ─────────────────────►
level ─────────────────────►

                              id
                              │
                              ▼
                         généré par
                         le serveur
```

---

# 43. Notre API complète

Nous pouvons maintenant imaginer notre première version :

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


class PlayerCreate(BaseModel):
    name: str = Field(min_length=3)
    score: int = Field(ge=0)
    level: int = Field(ge=1)


class Player(PlayerCreate):
    id: int


@app.get("/players")
def get_players():
    ...


@app.get("/players/{player_id}")
def get_player(player_id: int):
    ...


@app.post("/players")
def create_player(player: PlayerCreate):
    ...


@app.put("/players/{player_id}")
def update_player(
    player_id: int,
    player: PlayerCreate,
):
    ...


@app.delete("/players/{player_id}")
def delete_player(player_id: int):
    ...
```

Nous avons déjà la structure d'une véritable API REST.

---

# 44. Architecture conceptuelle

À ce stade, il faut avoir compris cette chaîne :

```text
                 HTTP
                  │
                  ▼
              FastAPI
                  │
             ┌────┴────┐
             ▼         ▼
          Routing   Validation
             │         │
             │      Pydantic
             │         │
             └────┬────┘
                  ▼
            Code Python
                  │
                  ▼
             Données
                  │
                  ▼
               JSON
```

Et parallèlement :

```text
             FastAPI
                │
       ┌────────┴────────┐
       ▼                 ▼
  Type Hints          Pydantic
       │                 │
       └────────┬────────┘
                ▼
             OpenAPI
                │
       ┌────────┴────────┐
       ▼                 ▼
  Swagger UI           ReDoc
     /docs             /redoc
```

---

# 45. Défi — concevoir une API

## 🎯 À vous de jouer

Notre jeu possède maintenant des **armes**.

Une arme possède :

```text
id
name
damage
weight
```

Proposez les endpoints nécessaires pour :

1. récupérer toutes les armes ;
2. récupérer une arme ;
3. créer une arme ;
4. modifier une arme ;
5. supprimer une arme.

Essayez de respecter les conventions REST.

---

# 46. Correction

Une solution possible :

```text
GET    /weapons
GET    /weapons/{weapon_id}

POST   /weapons

PUT    /weapons/{weapon_id}

DELETE /weapons/{weapon_id}
```

On retrouve :

```text
GET    → lecture
POST   → création
PUT    → modification
DELETE → suppression
```

---

# 47. Défi — définir le modèle Pydantic

Nous voulons qu'une arme respecte les règles suivantes :

```text
name   → au moins 3 caractères
damage → entier positif
weight → nombre positif
```

Comment définir le modèle ?

---

# 48. Correction

```python
from pydantic import BaseModel, Field


class WeaponCreate(BaseModel):
    name: str = Field(min_length=3)
    damage: int = Field(gt=0)
    weight: float = Field(gt=0)
```

FastAPI peut maintenant utiliser ce modèle pour :

* valider les requêtes ;
* générer le schéma OpenAPI ;
* documenter automatiquement les champs.

---

# 49. Défi — trouver l'information

Notre API est lancée.

Vous savez qu'elle possède :

```text
GET /players
POST /players
GET /weapons
POST /weapons
```

Mais vous ne connaissez pas tous les détails.

### Question

Comment découvrir automatiquement comment utiliser cette API ?

---

# 50. Réponse

Avec Swagger UI :

```text
/docs
```

ou avec ReDoc :

```text
/redoc
```

Et pour obtenir directement le contrat machine-readable :

```text
/openapi.json
```

---

# 51. Ce qu'il faut retenir

## API

Une API permet à des applications de communiquer entre elles.

```text
Client ←── HTTP ──→ Serveur
```

---

## REST

Une API REST organise généralement les opérations autour de ressources :

```text
GET
POST
PUT
DELETE
```

---

## FastAPI

FastAPI permet de créer rapidement des APIs Python.

```python
@app.get("/players")
def get_players():
    ...
```

---

## Pydantic

Pydantic permet de définir et valider les données :

```python
class Player(BaseModel):
    name: str
    score: int
```

---

## Type Hints

FastAPI exploite les annotations de type :

```python
player_id: int
```

---

## OpenAPI

OpenAPI décrit automatiquement notre API.

```text
/openapi.json
```

---

## Swagger UI

Swagger UI fournit une interface interactive :

```text
/docs
```

---

# 52. Le schéma à retenir

```text
                  CLIENT
                     │
                     │ HTTP
                     ▼
              ┌─────────────┐
              │   FastAPI   │
              └──────┬──────┘
                     │
             ┌───────┴───────┐
             ▼               ▼
          Routing        Pydantic
             │               │
             │          Validation
             │               │
             └───────┬───────┘
                     ▼
                Code Python
                     │
                     ▼
                   JSON
                     │
                     ▼
                  CLIENT


               FastAPI
                  │
          Type Hints + Pydantic
                  │
                  ▼
               OpenAPI
                  │
          ┌───────┴───────┐
          ▼               ▼
      Swagger UI         ReDoc
        /docs            /redoc
```

---

# 53. Pour le projet fil rouge

Pour la première partie de votre projet, vous devrez être capables de :

### 1. Créer une application FastAPI

```python
from fastapi import FastAPI

app = FastAPI()
```

### 2. Définir des routes

```python
@app.get("/...")
@app.post("/...")
@app.put("/...")
@app.delete("/...")
```

### 3. Utiliser les Type Hints

```python
player_id: int
```

### 4. Créer des modèles Pydantic

```python
class Player(BaseModel):
    ...
```

### 5. Valider les données

```python
score: int = Field(ge=0)
```

### 6. Définir les réponses

```python
response_model=Player
```

### 7. Vérifier la documentation

```text
/docs
/redoc
/openapi.json
```

---

# 54. La philosophie FastAPI

Une dernière idée à retenir :

> **Décrire correctement son API dans le code permet à FastAPI de faire beaucoup de travail automatiquement.**

```text
Code Python
    +
Type Hints
    +
Pydantic
    │
    ▼
FastAPI
    │
    ├──► Validation
    │
    ├──► Sérialisation
    │
    ├──► Gestion des erreurs
    │
    ├──► OpenAPI
    │
    └──► Swagger UI
```
