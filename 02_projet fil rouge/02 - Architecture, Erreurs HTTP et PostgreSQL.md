# 🚀 02 — Architecture Clean, Erreurs HTTP & Base PostgreSQL

- **Séances couvertes :** Séance 3 & Séance 4
- **Objectifs de la journée :**
  - Structurer proprement le projet avec `APIRouter` (Clean Architecture).
  - Gérer les erreurs HTTP avec les bons codes de statut (`400`, `403`, `404`).
  - Mettre en place un système de logs applicatif pour le Game Master (`gamemaster.log`).
  - Connecter l'API à une base de données PostgreSQL via l'ORM **SQLAlchemy**.

---

## 💼 Brief Client : Mission "DigitalEscape Studio"

> *"Le client DigitalEscape Studio formule deux demandes urgentes : premièrement, l'API doit retourner des codes de statut HTTP explicites lors des erreurs des joueurs (porte verrouillée, code erroné) et tracer chaque événement dans un journal de log pour les Game Masters. Deuxièmement, la progression des parties ne doit plus être perdue au redémarrage du serveur : vous devez raccorder votre moteur à la base de données PostgreSQL."*

---

## 🧩 Partie 1 : Modularité, Exceptions HTTP & Logs GM

### 🧠 Notions Théoriques Clés
- **`APIRouter`** : Découpage de l'application en modules indépendants (`app/routers/`).
- **`HTTPException`** : Levée d'erreurs HTTP standardisées avec payload JSON structuré.
- **Module `logging`** : Configuration d'un logger applicatif écrivant dans un fichier physique `.log`.

### 🎯 Travail à Réaliser en Équipe

#### Étape 1.1 : Séparation en APIRouters
Organisez vos routes dans des fichiers dédiés :
- `app/routers/player_game.py` (Actions du joueur)
- `app/routers/puzzles.py` (Gestion des énigmes)
- `app/routers/system.py` (Santé & supervision)

Incorporez ces routeurs dans `app/main.py` à l'aide de `app.include_router(...)`.

#### Étape 1.2 : Gestion rigoureuse des erreurs HTTP
Mettez à jour vos routes pour lever des `HTTPException` pertinentes :
- **`404 Not Found`** : Si le joueur demande une salle ou un puzzle qui n'existe pas.
- **`403 Forbidden`** : Si le joueur tente d'ouvrir un sas sans posséder la clé requise dans son inventaire.
- **`400 Bad Request`** : Si le joueur soumet une tentative sur une énigme déjà résolue.

#### Étape 1.3 : Configuration du Logging Game Master (`app/core/logging.py`)
Créez un module de journalisation pour enregistrer les actions dans `gamemaster.log` :

```python
import logging

logger = logging.getLogger("gamemaster")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("gamemaster.log")
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - GM_AUDIT - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
```

Dans vos routes, logguez chaque événement :
`logger.info(f"Joueur '{player_id}' a tente le puzzle '{puzzle_id}' -> STATUT: {status}")`

---

## 🧩 Partie 2 : Persistance DB avec PostgreSQL & SQLAlchemy

### 🧠 Notions Théoriques Clés
- **SQLAlchemy v2** : ORM (Object-Relational Mapping) permettant de manipuler la DB avec des objets Python.
- **Session DB (`get_db`)** : Injection de dépendance FastAPI pour ouvrir et fermer proprement une transaction SQL.

## 🐘 Installation et Configuration de PostgreSQL

Le projet utilise une base de données relationnelle **PostgreSQL**. Vous avez deux options au choix :

### Option A : Via Docker Desktop (Recommandé)
Si Docker est installé sur votre machine, lancez un conteneur PostgreSQL en une ligne :

```bash
docker run --name escape_postgres \
  -e POSTGRES_USER=escape_admin \
  -e POSTGRES_PASSWORD=escape_secret \
  -e POSTGRES_DB=escape_engine_db \
  -p 5432:5432 \
  -d postgres:16
```

### Option B : Installation Locale
Téléchargez PostgreSQL depuis [postgresql.org](https://www.postgresql.org/download/) et créez une base de données nommée `escape_engine_db` via `pgAdmin` ou `psql`.

### 🎯 Travail à Réaliser en Équipe

#### Étape 2.1 : Configuration de la Connexion (`app/database.py`)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### Étape 2.2 : Modèles SQLAlchemy (`app/models/`)
Créez les tables dans PostgreSQL :

1. **`UserModel`** (`app/models/user.py`) : `id`, `username`, `created_at`.
2. **`RoomModel`** (`app/models/room.py`) : `id`, `name`, `description`, `is_unlocked`.
3. **`PuzzleModel`** (`app/models/puzzle.py`) : `id`, `room_id`, `solution_code`, `is_solved`.

#### Étape 2.3 : Services CRUD & Intégration
Dans `app/services/engine_service.py`, réécrivez la logique de déverrouillage pour lire et mettre à jour la base PostgreSQL en direct lorsque le joueur résout une énigme !

---

## 🏁 Checklist de fin de TP

- [ ] Les routes de l'API sont découpées et organisées avec `APIRouter`.
- [ ] Tenter d'accéder à une salle inexistante renvoie un statut **`404 Not Found`** propre.
- [ ] Chaque tentative de résolution crée une ligne horodatée dans le fichier `gamemaster.log`.
- [ ] La base PostgreSQL contient les tables `users`, `rooms` et `puzzles`.
- [ ] Si vous redémarrez le serveur FastAPI, la salle déverrouillée reste enregistrée comme déverrouillée dans la base de données PostgreSQL ! 🐘
