# 🚀 03 — Relations SQL, Alembic, Tests Pytest & Auth JWT

- **Séances couvertes :** Séance 5 & Séance 6
- **Objectifs de la journée :**
  - Modéliser les relations SQL complexes (Salles <-> Objets <-> Inventaire Joueur).
  - Gérer les évolutions du schéma de base de données avec **Alembic**.
  - Automatiser la recette du jeu avec une suite de tests unitaires et d'intégration **Pytest**.
  - Sécuriser l'accès aux terminaux du jeu avec des **jetons JWT** et le hachage **bcrypt**.

---

## 💼 Brief Client : Mission "DigitalEscape Studio"

> *"Pour enrichir l'expérience de jeu, DigitalEscape Studio intègre la gestion des inventaires (un joueur peut ramasser des objets et les utiliser pour ouvrir des sas). De plus, l'accès au jeu doit être sécurisé : chaque joueur doit pouvoir créer son compte, se connecter avec son mot de passe et obtenir un token JWT pour interagir avec le moteur."*

---

## 🧩 Partie 1 : Relations SQL, Alembic & Tests Pytest

### 🧠 Notions Théoriques Clés
- **Relations SQLAlchemy** : `relationship()`, clés étrangères (`ForeignKey`), table de jonction Many-to-Many (`player_inventory`).
- **Alembic** : Outil officiel de migration de schéma pour SQLAlchemy.
- **Pytest** : Framework de test automatique avec fixtures et `httpx.AsyncClient` ou `TestClient`.

### 🎯 Travail à Réaliser en Équipe

#### Étape 1.1 : Modélisation des Relations SQL
1. Ajoutez la table d'association Many-to-Many `player_inventory` (`user_id`, `item_id`).
2. Dans `UserModel`, ajoutez la relation : `inventory = relationship("ItemModel", secondary="player_inventory")`.
3. Dans `RoomModel`, ajoutez la relation One-to-Many : `puzzles = relationship("PuzzleModel", back_populates="room")`.

#### Étape 1.2 : Configuration et Migration Alembic
Initialisez Alembic dans le projet :

```bash
alembic init alembic
```

1. Dans `alembic/env.py`, importez votre `Base` SQLAlchemy et vos modèles.
2. Générez la migration automatique :
   ```bash
   alembic revision --autogenerate -m "Add inventory and room relations"
   alembic upgrade head
   ```

#### Étape 1.3 : Écriture des Tests `pytest` (`tests/test_gameplay.py`)
Créez une suite de tests automatisés :
- Test de la création d'une salle et d'un puzzle.
- Test de la résolution d'une énigme et vérification du changement d'état du verrou en base.
- Exécutez `pytest` dans votre terminal.

---

## 🧩 Partie 2 : Authentification JWT & Sécurité des Mots de Passe

### 🧠 Notions Théoriques Clés
- **Hachage bcrypt** : Transformation irréversible du mot de passe avec sel (jamais de mot de passe en clair !).
- **JWT (JSON Web Token)** : Jeton cryptographique signé contenant l'identité de l'utilisateur (`sub`, `exp`).
- **OAuth2PasswordBearer** : Schéma d'authentification standard dans FastAPI.

### 🎯 Travail à Réaliser en Équipe

#### Étape 2.1 : Service de Sécurité (`app/core/security.py`)
Implémentez le hachage et la gestion des jetons :

```python
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jose.jwt as jwt
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
```

#### Étape 2.2 : Endpoints d'Authentification (`app/routers/auth.py`)
- `POST /auth/register` : Inscription d'un nouveau joueur (hachage du password avant insertion en DB).
- `POST /auth/login` : Ingestion des identifiants (OAuth2 form), vérification et retour du token JWT.
- `GET /auth/me` : Endpoint protégé retournant les infos du joueur connecté via la dépendance `get_current_user`.

#### Étape 2.3 : Protection des Routes du Jeu
Sécurisez vos routes d'exploration (`GET /rooms`, `POST /puzzles/submit`) en exigeant la dépendance `get_current_user` !

---

## 🏁 Checklist de fin de TP

- [ ] Les migrations Alembic s'exécutent proprement (`alembic upgrade head`).
- [ ] La commande `pytest` s'exécute avec 100% de succès dans la console.
- [ ] La table `users` dans PostgreSQL enregistre les mots de passe sous forme de hashes bcrypt (`$2b$...`).
- [ ] Il est impossible d'interagir avec le jeu sans envoyer le header `Authorization: Bearer <TOKEN_JWT>`. 🔒
