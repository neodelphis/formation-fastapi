# 🚀 06 — Consommation d'API Tierce, Mode Dégradé & Recette Finale

- **Séances couvertes :** Séance 11 & Séance 12
- **Objectifs de la journée :**
  - Consommer une API HTTP externe (Service d'Indices par IA ou Threat Intel) à l'aide de `httpx`.
  - Implémenter des timeouts stricts et un mode dégradé (Fallback) en cas de panne réseau.
  - Finaliser l'intégration complète de votre projet (API, PostgreSQL, JWT, RBAC, CLI, Tests).
  - Présenter votre solution lors de la soutenance finale devant le client / formateur.

---

## 💼 Brief Client : Mission "DigitalEscape Studio"

> *"Dernière ligne droite avant le lancement commercial ! Votre moteur de jeu doit interroger un service d'IA / Threat Intelligence externe pour fournir des indices dynamiques aux joueurs en difficulté. Attention : votre API doit rester 100% fonctionnelle même si ce service externe rencontre une panne ! Ensuite, vous présenterez votre projet complet lors de la recette finale."*

---

## 🧩 Partie 1 : APIs Tierces & Mode Dégradé (`app/services/hint_service.py`)

### 🧠 Notions Théoriques Clés
- **Requêtes HTTP Sortantes** : `httpx.AsyncClient` pour appeler un serveur tiers depuis votre backend.
- **Timeouts Stricts** : Éviter de bloquer l'API en définissant un délai limite (ex: 3.0s).
- **Mode Dégradé (Fallback)** : Stratégie de secours si le service externe ne répond pas.

### 🎯 Travail à Réaliser en Équipe

#### Étape 1.1 : Service d'Indices Externe (`app/services/hint_service.py`)
Créez un service pour interroger l'API d'indices distante (fournie par le formateur) :

```python
import httpx
from fastapi import HTTPException

EXTERNAL_HINT_API_URL = "http://127.0.0.1:9000/api/hints" # ou l'URL fournie

async def fetch_external_hint(puzzle_id: str) -> str:
    async with httpx.AsyncClient(timeout=3.0) as client:
        try:
            response = await client.post(EXTERNAL_HINT_API_URL, json={"puzzle_id": puzzle_id})
            response.raise_for_status()
            data = response.json()
            return data.get("hint", "Indice indisponible")
        except (httpx.TimeoutException, httpx.HTTPError):
            # Mode Dégradé (Fallback) : Retourner un indice local par défaut !
            return "Indice de secours local : Observez attentivement les objets de la salle."
```

#### Étape 1.2 : Endpoint de Demande d'Indice
Créez la route `POST /puzzles/{puzzle_id}/request-hint` accessible aux joueurs connectés.

#### Étape 1.3 : Test du Mode Dégradé
Simulez une panne en coupant le serveur externe : vérifiez que votre API ne plante pas et renvoie proprement l'indice de secours local !

---

## 🧩 Partie 2 : Finalisation, Recette & Soutenance Finale

### 🎯 Déroulé de la Recette Finale (Soutenance)

Chaque groupe dispose de **15 minutes** pour faire la démonstration de son moteur d'Escape Game devant le formateur :

#### 1. Préparation
- Vérifiez votre fichier `README.md` (instructions d'installation, lancement de PostgreSQL, exécution des migrations Alembic).
- Lancez la suite de tests `pytest` et vérifiez que **100% des tests sont au vert**.

#### 2. Démonstration en Direct (15 min par groupe)
- **Présentation (3 min)** : Thématique choisie par l'équipe et architecture des dossiers.
- **Démonstration Joueur (6 min)** : Inscription, Auth JWT, Exploration des salles via Swagger UI, résolution d'énigmes et déclenchement de l'énigme asynchrone Climax.
- **Démonstration Game Master (4 min)** : Supervision, override d'énigme à distance via la console CLI `gm-console`, consultation de l'audit trail et parsing de logs.
- **Questions & Réponses (2 min)** : Réponses aux questions techniques du formateur.

---

## 📊 Rappel de la Grille d'Évaluation (30 Points)

| Critère d'Évaluation | Barème |
| :--- | :---: |
| **1. Structure & Clean Architecture** (Routage, typage, propreté du code) | **/ 4 pts** |
| **2. API REST & Validation Pydantic** (Verbes HTTP, schemas stricts) | **/ 4 pts** |
| **3. Base de Données PostgreSQL & ORM** (Modèles, Alembic, CRUD) | **/ 4 pts** |
| **4. Sécurité, Auth JWT & RBAC** (bcrypt, JWT, rôles Player/GM) | **/ 5 pts** |
| **5. Traitements Asynchrones (`async`)** (Utilisation de `asyncio.gather`) | **/ 3 pts** |
| **6. Scripting Forensics & Console CLI** (Parsing Regex & CLI `argparse`) | **/ 4 pts** |
| **7. API Tierce & Mode Dégradé** (Appel HTTP avec timeout & fallback) | **/ 3 pts** |
| **8. Tests & Documentation** (Tests Pytest & README/Swagger) | **/ 3 pts** |
| **TOTAL** | **/ 30 pts** |

Félicitations pour le travail accompli tout au long de ce projet fil rouge ! 🎓
