# Séance 3 — Structuration, erreurs et logging

## FastAPI · Architecture · Gestion des erreurs · Logging · Debugging

> **Version exécutable des exemples**

Tous les exemples de cette séance utilisent la même structure de projet afin de pouvoir être exécutés progressivement.

---

# 1. Structure du projet

Nous allons construire :

```text
game-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── player.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   └── players.py
│   │
│   └── services/
│       ├── __init__.py
│       └── player_service.py
│
└── requirements.txt
```

Les fichiers `__init__.py` peuvent être vides.

---

# 2. Installation

Créer l'environnement virtuel :

```bash
python -m venv .venv
```

Linux / macOS :

```bash
source .venv/bin/activate
```

Windows :

```powershell
.venv\Scripts\activate
```

Installer FastAPI :

```bash
pip install "fastapi[standard]"
```

---

# 3. Les modèles Pydantic

Fichier :

```text
app/models/player.py
```

```python
from pydantic import BaseModel, Field


class PlayerCreate(BaseModel):
    name: str = Field(min_length=3)
    score: int = Field(ge=0)
    level: int = Field(ge=1)


class Player(PlayerCreate):
    id: int
```

Nous avons deux modèles.

### `PlayerCreate`

Représente les données nécessaires pour créer un joueur :

```json
{
    "name": "Alice",
    "score": 1200,
    "level": 12
}
```

### `Player`

Représente un joueur complet :

```json
{
    "id": 1,
    "name": "Alice",
    "score": 1200,
    "level": 12
}
```

L'`id` est ajouté par le serveur.

---

# 4. Le service

Fichier :

```text
app/services/player_service.py
```

```python
from app.models.player import Player, PlayerCreate


players: list[Player] = [
    Player(
        id=1,
        name="Alice",
        score=1200,
        level=12,
    ),
    Player(
        id=2,
        name="Bob",
        score=950,
        level=9,
    ),
]


def get_players() -> list[Player]:
    return players


def get_player(player_id: int) -> Player | None:
    for player in players:
        if player.id == player_id:
            return player

    return None


def create_player(player_data: PlayerCreate) -> Player:
    new_id = max(
        (player.id for player in players),
        default=0,
    ) + 1

    player = Player(
        id=new_id,
        **player_data.model_dump(),
    )

    players.append(player)

    return player
```

---

# 5. Pourquoi le service utilise-t-il Pydantic ?

Le service reçoit :

```python
player_data: PlayerCreate
```

Il travaille donc avec un objet Python validé par Pydantic.

Pour transformer cet objet en dictionnaire :

```python
player_data.model_dump()
```

Par exemple :

```python
player_data.model_dump()
```

produit :

```python
{
    "name": "Charlie",
    "score": 1000,
    "level": 1,
}
```

---

# 6. Le router

Fichier :

```text
app/routers/players.py
```

```python
from fastapi import APIRouter, HTTPException

from app.models.player import Player, PlayerCreate
from app.services import player_service


router = APIRouter(
    prefix="/players",
    tags=["players"],
)


@router.get("", response_model=list[Player])
def list_players() -> list[Player]:
    return player_service.get_players()


@router.get("/{player_id}", response_model=Player)
def get_player(player_id: int) -> Player:
    player = player_service.get_player(player_id)

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

    return player


@router.post(
    "",
    response_model=Player,
    status_code=201,
)
def create_player(player: PlayerCreate) -> Player:
    return player_service.create_player(player)
```

Nous avons maintenant trois endpoints fonctionnels :

```text
GET  /players
GET  /players/{player_id}
POST /players
```

---

# 7. Le fichier principal

Fichier :

```text
app/main.py
```

```python
from fastapi import FastAPI

from app.routers.players import router as players_router


app = FastAPI(
    title="Game API",
    description="API de démonstration pour le cours",
    version="1.0.0",
)


app.include_router(players_router)
```

---

# 8. Lancer l'application

Depuis le dossier `game-api` :

```bash
fastapi dev app/main.py
```

L'application est disponible à :

```text
http://127.0.0.1:8000
```

---

# 9. Tester la liste des joueurs

Ouvrir :

```text
http://127.0.0.1:8000/players
```

Résultat :

```json
[
    {
        "id": 1,
        "name": "Alice",
        "score": 1200,
        "level": 12
    },
    {
        "id": 2,
        "name": "Bob",
        "score": 950,
        "level": 9
    }
]
```

---

# 10. Tester un joueur

Ouvrir :

```text
http://127.0.0.1:8000/players/1
```

Résultat :

```json
{
    "id": 1,
    "name": "Alice",
    "score": 1200,
    "level": 12
}
```

---

# 11. Tester un joueur inexistant

Ouvrir :

```text
http://127.0.0.1:8000/players/999
```

Résultat :

```json
{
    "detail": "Player not found"
}
```

Code HTTP :

```text
404 Not Found
```

---

# 12. Tester une mauvaise valeur

Essayer :

```text
http://127.0.0.1:8000/players/abc
```

FastAPI détecte que :

```python
player_id: int
```

nécessite un entier.

La route n'est donc pas exécutée.

FastAPI renvoie automatiquement une erreur de validation.

---

# 13. Créer un joueur

Nous pouvons utiliser Swagger UI.

Ouvrir :

```text
http://127.0.0.1:8000/docs
```

Sélectionner :

```text
POST /players
```

Puis :

```text
Try it out
```

Envoyer :

```json
{
    "name": "Charlie",
    "score": 1000,
    "level": 1
}
```

La réponse doit être :

```text
201 Created
```

avec :

```json
{
    "id": 3,
    "name": "Charlie",
    "score": 1000,
    "level": 1
}
```

---

# 14. Tester la validation Pydantic

Envoyer :

```json
{
    "name": "A",
    "score": -10,
    "level": 0
}
```

Plusieurs contraintes sont violées :

```text
name
→ minimum 3 caractères

score
→ supérieur ou égal à 0

level
→ supérieur ou égal à 1
```

FastAPI/Pydantic rejette automatiquement la requête.

---

# 15. Ajouter les logs

Nous allons maintenant modifier le service.

Fichier :

```text
app/services/player_service.py
```

Ajouter :

```python
import logging
```

Puis :

```python
logger = logging.getLogger(__name__)
```

Le début du fichier devient :

```python
import logging

from app.models.player import Player, PlayerCreate


logger = logging.getLogger(__name__)


players: list[Player] = [
    Player(
        id=1,
        name="Alice",
        score=1200,
        level=12,
    ),
    Player(
        id=2,
        name="Bob",
        score=950,
        level=9,
    ),
]
```

---

# 16. Ajouter un log dans `get_players`

```python
def get_players() -> list[Player]:
    logger.info("Retrieving all players")

    return players
```

Lorsque la route est appelée, le service produit un log.

---

# 17. Logger la recherche d'un joueur

```python
def get_player(player_id: int) -> Player | None:
    logger.info(
        "Searching for player %s",
        player_id,
    )

    for player in players:
        if player.id == player_id:
            logger.info(
                "Player %s found",
                player_id,
            )

            return player

    logger.warning(
        "Player %s not found",
        player_id,
    )

    return None
```

---

# 18. Observer les logs

Lancer :

```bash
fastapi dev app/main.py
```

Puis appeler :

```text
GET /players/1
```

Dans le terminal, on peut observer les messages produits par l'application.

Par exemple :

```text
INFO Searching for player 1
INFO Player 1 found
```

---

# 19. Ajouter des logs à la création

```python
def create_player(player_data: PlayerCreate) -> Player:
    new_id = max(
        (player.id for player in players),
        default=0,
    ) + 1

    player = Player(
        id=new_id,
        **player_data.model_dump(),
    )

    players.append(player)

    logger.info(
        "Player %s created",
        player.id,
    )

    return player
```

---

# 20. Logger une erreur attendue

Dans le router :

```python
@router.get("/{player_id}", response_model=Player)
def get_player(player_id: int) -> Player:
    player = player_service.get_player(player_id)

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

    return player
```

Le service produit déjà :

```python
logger.warning(
    "Player %s not found",
    player_id,
)
```

Puis le router transforme cette situation en :

```text
404 Not Found
```

---

# 21. Pourquoi le service ne lève-t-il pas directement `HTTPException` ?

Parce que nous voulons éviter de mélanger les responsabilités.

Le service sait :

> « Le joueur n'existe pas. »

Le router sait :

> « Une ressource inexistante doit être représentée par une réponse HTTP 404. »

On obtient :

```text
Service
   │
   │ Player not found
   ▼
Router
   │
   │ HTTP 404
   ▼
Client
```

Cette séparation sera particulièrement utile lorsque nous introduirons des tests et une base de données.

---

# 22. Exemple de niveau `DEBUG`

Nous pouvons également utiliser :

```python
logger.debug(
    "Current players: %s",
    players,
)
```

Mais les logs `DEBUG` sont généralement destinés aux informations très détaillées.

Par exemple :

```text
DEBUG Searching in 15 players
DEBUG Current player ID: 8
DEBUG Current player ID: 9
DEBUG Current player ID: 10
```

Ce niveau peut être utile pendant le développement.

---

# 23. Les niveaux de logging

```python
logger.debug("Detailed information")
logger.info("Normal application event")
logger.warning("Something unexpected happened")
logger.error("An error occurred")
logger.exception("An exception occurred")
```

À retenir :

```text
DEBUG
  ↓
INFO
  ↓
WARNING
  ↓
ERROR
  ↓
CRITICAL
```

Plus on descend, plus la situation est grave.

---

# 24. `logger.exception()`

Lorsqu'une exception est capturée :

```python
try:
    result = perform_operation()

except Exception:
    logger.exception(
        "Unexpected error during operation"
    )
    raise
```

Le `raise` est important.

Il permet de ne pas masquer l'erreur.

---

# 25. Exemple de service avec exception

Imaginons temporairement :

```python
def dangerous_operation() -> float:
    try:
        result = 10 / 0
        return result

    except Exception:
        logger.exception(
            "Unexpected error during calculation"
        )
        raise
```

Le log contient la trace de l'exception.

Le développeur peut alors identifier :

```text
ZeroDivisionError
```

et la ligne concernée.

---

# 26. À ne pas faire

Éviter :

```python
try:
    ...
except Exception:
    return {
        "error": "Something went wrong"
    }
```

Pourquoi ?

Parce que l'erreur réelle disparaît.

On perd :

* le type de l'exception ;
* la trace ;
* la ligne concernée ;
* le contexte.

Pour debugger, c'est problématique.

---

# 27. Une erreur HTTP attendue

Pour une erreur connue :

```python
if player is None:
    raise HTTPException(
        status_code=404,
        detail="Player not found",
    )
```

C'est approprié.

---

# 28. Une exception inattendue

Pour une erreur que nous n'avions pas prévue :

```python
try:
    ...
except Exception:
    logger.exception(
        "Unexpected error"
    )
    raise
```

C'est une situation différente.

```text
Erreur connue
     ↓
HTTPException
     ↓
Réponse HTTP contrôlée


Erreur inattendue
     ↓
Logging
     ↓
Exception
     ↓
Investigation
```

---

# 29. Architecture complète

Nous avons maintenant :

```text
app/
│
├── main.py
│
├── models/
│   └── player.py
│
├── routers/
│   └── players.py
│
└── services/
    └── player_service.py
```

Le flux d'une requête est :

```text
                    Client
                      │
                      │ HTTP
                      ▼
              ┌──────────────┐
              │    Router    │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │   Service    │
              └──────┬───────┘
                     │
                     ▼
                  Données
```

---

# 30. Où interviennent Pydantic et les logs ?

```text
                    Client
                      │
                      │ JSON
                      ▼
              ┌──────────────┐
              │    FastAPI   │
              └──────┬───────┘
                     │
               Validation
                     │
                  Pydantic
                     │
                     ▼
              ┌──────────────┐
              │    Router    │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │   Service    │
              └──────┬───────┘
                     │
                     ▼
                  Données

              Logging
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
    Router    Service   Erreurs
```

---

# 31. Vérifier la documentation

Une fois le serveur lancé :

```text
http://127.0.0.1:8000/docs
```

Nous devons voir le groupe :

```text
players
```

avec :

```text
GET    /players
GET    /players/{player_id}
POST   /players
```

Le modèle `PlayerCreate` doit également apparaître dans la documentation.

---

# 32. Vérifier OpenAPI

Ouvrir :

```text
http://127.0.0.1:8000/openapi.json
```

Le document doit contenir notamment :

```text
paths
components
schemas
```

Les modèles Pydantic sont utilisés pour générer les schémas.

---

# 33. Tester avec `curl`

Swagger est pratique, mais nous pouvons également utiliser `curl`.

### Liste

```bash
curl http://127.0.0.1:8000/players
```

### Joueur

```bash
curl http://127.0.0.1:8000/players/1
```

### Joueur inexistant

```bash
curl http://127.0.0.1:8000/players/999
```

---

# 34. Créer un joueur avec `curl`

Linux / macOS :

```bash
curl \
  -X POST \
  http://127.0.0.1:8000/players \
  -H "Content-Type: application/json" \
  -d '{"name":"Charlie","score":1000,"level":1}'
```

Windows PowerShell peut nécessiter une syntaxe différente ; Swagger UI est donc souvent plus simple pendant le cours.

Réponse :

```json
{
    "id": 3,
    "name": "Charlie",
    "score": 1000,
    "level": 1
}
```

---

# 35. Attention : nos données ne sont pas persistantes

Notre service utilise :

```python
players: list[Player] = [...]
```

Cela signifie que les données sont conservées uniquement en mémoire.

Si nous arrêtons le serveur :

```text
Ctrl + C
```

puis le relançons :

```bash
fastapi dev app/main.py
```

le joueur `Charlie` a disparu.

C'est normal.

---

# 36. Pourquoi avoir commencé ainsi ?

Parce que nous voulons distinguer deux problèmes :

```text
Problème 1
Comment structurer une API ?

Problème 2
Comment stocker durablement les données ?
```

Nous avons traité le premier.

Le second sera traité lorsque nous introduirons une base de données.

---

# 37. Défi — trouver la couche responsable

Pour chaque situation, indiquez où se trouve principalement le problème.

### A

```text
GET /players/abc
```

`player_id` doit être un entier.

### B

```text
GET /players/999
```

Le joueur n'existe pas.

### C

La base de données refuse la connexion.

### D

Un joueur ne peut pas modifier son score après la fin d'une partie.

---

# 38. Correction

### A

```text
Validation FastAPI / Pydantic
```

### B

```text
Service
+
gestion HTTP dans le router
```

### C

```text
Accès aux données / infrastructure
```

### D

```text
Service
```

Il s'agit d'une règle métier.

---

# 39. Défi — refactorisation

Imaginez le code suivant :

```python
@app.post("/players")
def create_player(player: PlayerCreate):

    # Vérification
    if player.score < 0:
        ...

    # Génération ID
    ...

    # Sauvegarde
    ...

    # Calcul du niveau
    ...

    # Retour HTTP
    ...
```

Quel est le problème ?

La route fait trop de choses.

---

# 40. Une meilleure organisation

```text
Router
   │
   │ reçoit la requête
   ▼
Service
   │
   │ applique les règles métier
   ▼
Repository
   │
   │ sauvegarde
   ▼
Database
```

La route devient :

```python
@router.post(
    "",
    response_model=Player,
    status_code=201,
)
def create_player(player: PlayerCreate) -> Player:
    return player_service.create_player(player)
```

C'est beaucoup plus lisible.

---

# 41. Ce que nous avons gagné

### Avant

```text
main.py
    │
    ├── routes
    ├── modèles
    ├── logique métier
    ├── données
    ├── erreurs
    └── logs
```

### Après

```text
app/
│
├── main.py
│
├── models/
│
├── routers/
│
└── services/
```

Chaque partie a une responsabilité plus claire.

---

# 42. Architecture cible

Pour une application plus complète, nous pourrons progressivement arriver à :

```text
app/
│
├── main.py
│
├── routers/
│   ├── players.py
│   ├── weapons.py
│   └── games.py
│
├── services/
│   ├── player_service.py
│   ├── weapon_service.py
│   └── game_service.py
│
├── models/
│   ├── player.py
│   ├── weapon.py
│   └── game.py
│
├── repositories/
│
├── database/
│
└── tests/
```

Nous n'avons pas besoin de tout créer maintenant.

L'architecture doit évoluer avec les besoins.

---

# 43. Les trois idées importantes de cette séance

## 1. Séparer les responsabilités

```text
Router
Service
Model
```

---

## 2. Gérer correctement les erreurs

```text
4xx → problème lié à la requête
5xx → problème côté serveur
```

---

## 3. Observer son application

```text
Logs
+
Debugger
+
Tests
```

permettent de comprendre les problèmes au lieu de simplement les subir.

---

# 44. À retenir

Une API professionnelle ne consiste pas uniquement à créer des endpoints.

Elle doit aussi être :

```text
        ┌───────────────┐
        │     API       │
        └───────┬───────┘
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
   Structurée  Fiable  Observable
       │        │        │
       ▼        ▼        ▼
    Routers   Erreurs   Logs
    Services  HTTP      Debug
    Models
```

---

# 45. Checklist du projet

## Structure

* [ ] `main.py` contient principalement la configuration de l'application.
* [ ] Les endpoints sont organisés dans des routers.
* [ ] Les modèles Pydantic sont séparés.
* [ ] La logique métier est dans les services.

## HTTP

* [ ] Les routes utilisent les bons verbes HTTP.
* [ ] Les ressources inexistantes renvoient `404`.
* [ ] Les créations renvoient `201`.
* [ ] Les erreurs de validation sont correctement gérées.

## Logging

* [ ] Les événements importants sont journalisés.
* [ ] Les logs donnent suffisamment de contexte.
* [ ] Les exceptions inattendues sont enregistrées.
* [ ] Aucune information sensible n'est journalisée.

## Debugging

* [ ] Le problème peut être reproduit.
* [ ] Le code HTTP est vérifié.
* [ ] Les logs sont consultés.
* [ ] La couche responsable est identifiée.

---

# 46. Transition

Notre architecture est maintenant prête à accueillir une vraie source de données.

Jusqu'ici :

```text
Router
   ↓
Service
   ↓
liste Python
```

La prochaine étape sera :

```text
Router
   ↓
Service
   ↓
Repository
   ↓
SQLAlchemy
   ↓
Base de données
```

Nous passerons ainsi d'une API qui fonctionne uniquement en mémoire à une API capable de **persister ses données**.
