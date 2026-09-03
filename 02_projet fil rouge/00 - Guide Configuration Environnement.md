# 🛠️ Guide d'Installation et Configuration de l'Environnement

Bienvenue dans le projet fil rouge **EscapeEngine API** ! 

Ce document vous guide pas à pas pour installer et configurer un environnement de développement Python professionnel et propre sur votre machine (Windows, macOS ou Linux).

---

## 📌 1. Prérequis Systèmes

Avant de commencer, vérifiez que vous disposez des éléments suivants :
- **Python 3.11 ou supérieur**
- **Git**
- **VS Code** (ou un IDE Python de votre choix)
- **Docker Desktop** (recommandé pour PostgreSQL) ou un installateur local PostgreSQL.

---

## 🐍 2. Vérification & Installation de Python

Ouvrez votre terminal (PowerShell sur Windows, Terminal sur macOS/Linux) et vérifiez votre version de Python :

```bash
python --version
# ou
python3 --version
```

> ⚠️ **Important** : Si votre version est inférieure à 3.11, téléchargez et installez la version 3.11+ depuis [python.org](https://www.python.org/downloads/). Sur Windows, pensez à cocher la case **"Add Python to PATH"** lors de l'installation.

---

## 💻 3. Configuration de l'IDE (VS Code)

Nous vous recommandons **Visual Studio Code**. Installez les extensions suivantes depuis l'onglet Extensions (`Ctrl+Shift+X` ou `Cmd+Shift+X`) :

1. **Python** (Microsoft) — Support complet du langage.
2. **Pylance** (Microsoft) — Analyse statique et auto-complétion intelligente.
3. **SQLite Viewer** (Florian Kleinecke) — Visualisation rapide des bases locales.
4. **Thunder Client** ou **REST Client** — Pour tester vos endpoints d'API directement dans VS Code (alternative pratique à Postman).
5. **Ruff** (Charliermarsh) — Linter et formateur de code hyper rapide.

---

## 📦 4. Initialisation du Projet & Environnement Virtuel (`venv`)

Chaque groupe doit créer son propre dépôt Git et initialiser un environnement virtuel Python isolé.

### Étape 4.1 : Structure initiale des dossiers
Dans votre terminal, créez votre dossier de projet :

```bash
mkdir escape_engine_api
cd escape_engine_api
```

Créez l'arborescence recommandée :

```bash
mkdir -p app/core app/models app/schemas app/routers app/services scripts cli tests data
```

### Étape 4.2 : Création du Virtual Environment (`venv`)

```bash
# Sur macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Sur Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> 💡 **Astuce** : Lorsque votre environnement virtuel est activé, son nom `(.venv)` apparaît au début de votre ligne de commande dans le terminal.

### Étape 4.3 : Fichier `.gitignore`
Créez un fichier `.gitignore` à la racine pour éviter de pousser votre environnement virtuel et vos secrets sur Git :

```text
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
*.db
*.log
.gm_session
```

---

## ⚡ 5. Installation des Dépendances du Projet

Créez un fichier `pyproject.toml` ou `requirements.txt` à la racine de votre projet.

### Fichier `requirements.txt` :
```text
fastapi>=0.110.0
uvicorn[standard]>=0.28.0
pydantic>=2.6.0
pydantic-settings>=2.2.0
sqlalchemy>=2.0.28
alembic>=1.13.1
psycopg2-binary>=2.9.9
asyncpg>=0.29.0
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
httpx>=0.27.0
pytest>=8.0.0
pytest-asyncio>=0.23.5
```

Installez l'ensemble des dépendances avec la commande :

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔑 6. Variables d'Environnement (`.env`)

Créez un fichier `.env` à la racine de votre projet (basé sur un modèle `.env.example`) :

```env
# Configuration de l'Application
APP_NAME="EscapeEngine API"
ENVIRONMENT="development"
DEBUG=True

# Base de Données PostgreSQL
# DATABASE_URL="postgresql://escape_admin:escape_secret@localhost:5432/escape_engine_db"

# Sécurité & JWT
# SECRET_KEY="votre_cle_secrete_hyper_securisee_a_changer_absolument"
# ALGORITHM="HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## ✅ 7. Test de Validation de l'Environnement

Pour vérifier que tout fonctionne, créez un fichier `app/main.py` de test minimal :

```python
from fastapi import FastAPI

app = FastAPI(title="EscapeEngine API Test")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Environnement prêt pour l'Escape Game !"}
```

Lancez le serveur de développement Uvicorn :

```bash
uvicorn app.main:app --reload
```

Ouvrez votre navigateur sur :
- **API** : `http://127.0.0.1:8000`
- **Documentation Swagger** : `http://127.0.0.1:8000/docs`

Si l'interface Swagger s'affiche avec succès, **votre environnement est 100% opérationnel** ! 🚀
