# 🚀 04 — Sécurité RBAC, Audit Trail & Programation Asynchrone

- **Séances couvertes :** Séance 7 & Séance 8
- **Objectifs de la journée :**
  - Mettre en place un contrôle d'accès basé sur les rôles (RBAC) pour isoler les privilèges Joueurs et Game Masters.
  - Journaliser toutes les opérations sensibles dans une table d'audit (`audit_events`).
  - Concevoir une énigme "Climax" asynchrone exploitant `asyncio.gather()` pour effectuer des traitements parallèles non-bloquants.

---

## 💼 Brief Client : Mission "DigitalEscape Studio"

> *"Attribution des privilèges ! DigitalEscape Studio exige une séparation stricte des accès : un joueur standard ne doit en aucun cas pouvoir invoquer une commande réservée au Game Master. De plus, les Game Masters demandent une traçabilité d'audit complète. Enfin, pour l'énigme finale du jeu, vous devez concevoir un mécanisme à déchiffrement parallèle rapide qui échouera si votre backend n'utilise pas la programmation asynchrone `async/await`."*

---

## 🧩 Partie 1 : Autorisation RBAC & Audit Trail (`app/routers/gm_control.py`)

### 🧠 Notions Théoriques Clés
- **RBAC (Role-Based Access Control)** : Restreindre l'accès aux endpoints selon le rôle (`ROLE_PLAYER`, `ROLE_GAME_MASTER`).
- **Audit Trail** : Enregistrement immuable des actions critiques (qui, quoi, quand, résultat).

### 🎯 Travail à Réaliser en Équipe

#### Étape 1.1 : Modélisation des Rôles Utilisateurs
1. Ajoutez une colonne `role: str` dans la table `users` (valeur par défaut : `"ROLE_PLAYER"`).
2. Créez une dépendance FastAPI de vérification de rôle :

```python
from fastapi import HTTPException, status, Depends
from app.schemas.auth import UserResponse
from app.routers.auth import get_current_user

class RequireRole:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: UserResponse = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Privilèges insuffisants pour cette action Game Master"
            )
        return current_user
```

#### Étape 1.2 : Endpoints Exclusifs Game Master (`app/routers/gm_control.py`)
Déclarez les routes protégées par `Depends(RequireRole(["ROLE_GAME_MASTER"]))` :
- `POST /gm/override-puzzle` : Force la résolution d'une énigme à distance pour débloquer des joueurs.
- `GET /gm/audit-logs` : Consulte la liste des événements d'audit enregistrés en base.

#### Étape 1.3 : Table d'Audit (`app/models/audit.py`)
Créez la table `audit_events` (`id`, `user_id`, `action`, `resource`, `timestamp`, `status`) et insérez une ligne lors de chaque action d'override Game Master.

---

## 🧩 Partie 2 : Énigme Asynchrone Multi-Flux (`async/await`)

### 🧠 Notions Théoriques Clés
- **Loop d'Événements (Event Loop)** : Gestion concurrente des tâches I/O non-bloquantes en Python.
- **`asyncio.gather(*tasks)`** : Lancement simultané de plusieurs coroutines asynchrones.

### 🎯 Travail à Réaliser en Équipe

#### Étape 2.1 : Simulation des Capteurs / Sous-Systèmes (`app/services/async_solvers.py`)
Créez 4 coroutines simulées simulant l'interrogation de sous-systèmes distants du jeu :

```python
import asyncio
import random

async def verify_subsystem_alpha() -> bool:
    await asyncio.sleep(0.8) # Simulation I/O
    return True

async def verify_subsystem_beta() -> bool:
    await asyncio.sleep(0.8)
    return True

async def verify_subsystem_gamma() -> bool:
    await asyncio.sleep(0.8)
    return True

async def verify_subsystem_delta() -> bool:
    await asyncio.sleep(0.8)
    return True
```

#### Étape 2.2 : Endpoint Climax Asynchrone
Créez l'endpoint `POST /puzzles/climax-override` :

- **Méthode Synchrone (Bloquante - Échec)** : Si vous exécutiez les 4 appels l'un après l'autre, le temps total serait de 4 x 0.8s = 3.2 secondes -> **Trop lent !**
- **Méthode Asynchrone (Optimisée - Succès)** : Utilisez `asyncio.gather()` :

```python
results = await asyncio.gather(
    verify_subsystem_alpha(),
    verify_subsystem_beta(),
    verify_subsystem_gamma(),
    verify_subsystem_delta()
)
```

Mesurez le temps de réponse : l'endpoint répond en **~0.8 seconde** !

---

## 🏁 Checklist de fin de TP

- [ ] Un utilisateur `ROLE_PLAYER` reçoit un statut **`403 Forbidden`** s'il tente d'invoquer les routes d'override Game Master.
- [ ] Chaque opération Game Master enregistre une ligne dans la table PostgreSQL `audit_events`.
- [ ] L'endpoint `/puzzles/climax-override` utilise `asyncio.gather()` et répond en moins d'une seconde. ⚡
