# Guide Formateur — Projet Fil Rouge : "EscapeEngine API (Plateforme SaaS d'Escape Games)"

---

## 📋 Présentation Générale du Projet Fil Rouge

Le projet fil rouge **EscapeEngine API** place les étudiants (travaillant en équipes de 2 à 4) dans la peau d'une **équipe de développeurs backend / Game Masters**. 

Ils ont été mandatés par une entreprise d'Escape Games en ligne (*"DigitalEscape Studio"*) pour concevoir, développer et livrer le **moteur applicatif (API REST Backend + Console CLI)** d'un tout nouveau jeu d'escape game interactif.

### 💡 Principes Pédagogiques Clés
1. **Cadre Professionnel Réaliste** : Les étudiants répondent à un cahier des charges client (DigitalEscape Studio). Ils ne "jouent" pas artificiellement dans le jeu, mais conçoivent l'infrastructure backend d'un jeu pour leurs futurs utilisateurs (Joueurs & Game Masters).
2. **Liberté Créative sur la Thématique** : Chaque groupe d'étudiants choisit la thématique et le scénario de son Escape Game (ex: *Piratage Cyberpunk*, *Manoir Hanté*, *Station Spatiale en Dérive*, *Infiltration Médiévale*, *Braquage de Banque*, etc.).
3. **Même Socle Technique Exigé pour Tous** : Quelle que soit la thématique choisie, chaque projet doit respecter la même matrice de spécifications techniques (endpoints REST, schemas Pydantic, modèles PostgreSQL, Auth JWT, RBAC, Async/Await, Scripting et Console CLI).
4. **Progression par Séance (3h)** : **1 Séance (3h) = 1 Module Technique + 1 Fonctionnalité du Moteur Livrée au Client.**
5. **Double Perspective Joueur / Game Master (GM)** : L'API doit gérer les actions des **Joueurs** (explorer, résoudre, utiliser des objets) et les pouvoirs des **Game Masters** (superviser, débloquer une porte à distance, auditer les logs, lancer des indices).

---

## 🏗️ Architecture Globale du Projet Cible (`escape_engine_api`)

À la fin de la séance 12, le dépôt livré par chaque groupe doit respecter l'organisation suivante :

```text
escape_engine_api/
├── app/
│   ├── main.py                  # Point d'entrée FastAPI
│   ├── config.py                # Configuration & variables d'environnement (pydantic-settings)
│   ├── database.py              # Connexion PostgreSQL & session SQLAlchemy
│   ├── core/
│   │   ├── security.py          # Hachage bcrypt, génération/validation JWT
│   │   └── logging.py           # Configuration du logger structuré (joueurs & GM)
│   ├── models/                  # Modèles SQLAlchemy (Persistance DB)
│   │   ├── user.py              # Joueurs et Game Masters (roles)
│   │   ├── room.py              # Salles de l'Escape Game
│   │   ├── item.py              # Objets & inventaires
│   │   ├── puzzle.py            # Énigmes et verrous
│   │   └── audit.py             # Traçabilité des actions GM / Joueurs
│   ├── schemas/                 # Modèles Pydantic (DTO & Validation API)
│   │   ├── auth.py
│   │   ├── room.py
│   │   ├── puzzle.py
│   │   └── audit.py
│   ├── routers/                 # Endpoints FastAPI
│   │   ├── auth.py              # Inscription / Connexion Joueurs & GM
│   │   ├── player_game.py       # API Joueur (exploration, soumissions)
│   │   ├── gm_control.py        # API Game Master (supervision, override, audit)
│   │   └── external.py          # Service d'indices / Threat Intel externe
│   └── services/                # Logique métier du jeu
│       ├── engine_service.py
│       ├── async_solvers.py
│       └── hint_service.py
├── scripts/
│   ├── parse_session_logs.py    # Script d'analyse forensics / audit de partie
│   └── seed_game_data.py        # Script d'initialisation du scénario choisi
├── cli/
│   └── gm_console.py            # Console CLI d'administration Game Master (argparse)
├── tests/
│   ├── test_auth.py
│   ├── test_gameplay.py
│   └── test_async_solvers.py
├── alembic/                     # Migrations de base de données
├── .env.example
├── pyproject.toml
└── README.md
```

---

## 📅 Déroulé Détaillé Séance par Séance (12 × 3h = 36h)

---

### 🟢 Séance 1 — Cadrage du Projet, POO Python & Modélisation du Moteur

- **Durée :** 3 h  
- **Module :** M0 — Environnement, typage et Révision POO
- **Focus Cyber/Technique :** Classes, héritage, polymorphisme, `dataclasses`, Type Hints, découpage de modules Python.

#### 💬 Brief Client pour le Groupe (Pitch Formateur)
> *"DigitalEscape Studio vous confie la réalisation du moteur de leur nouveau jeu. Première étape : définir votre thématique (Cyber, SF, Horreur...) et modéliser orienté-objet les briques fondamentales du moteur de jeu (Salles, Sas/Portes, Énigmes, Objets)."*

#### ⚙️ Spécifications Backend à développer
Modéliser le domaine applicatif dans `app/domain/` avec des classes orientées objet :
- Classe mère `GameElement` (`id`, `name`, `description`).
- Classe `Room(GameElement)` contenant une liste d'`Item` et de `Door`.
- Classe `Door(GameElement)` avec état `is_locked`, `required_item_id`.
- Polymorphisme sur la classe `Puzzle` : `CodePuzzle` (code secret), `HashPuzzle` (empreinte/mot de passe), `LogicPuzzle`.
- Méthode `to_dict()` polymorphe pour faciliter la future sérialisation JSON.

#### 📋 Déroulé Pédagogique Formateur
1. **Cadrage & Brainstorming Groupe (30 min) :** Présentation du rôle de Game Master/Dev et validation de la thématique choisie par chaque groupe.
2. **Intro Technique (30 min) :** Rappels POO Python modernes (Type Hints, dataclasses, héritage, méthodes magiques).
3. **TP en Équipe (1h30) :** Implémentation des classes du domaine et du module d'inventaire.
4. **Débrief (30 min) :** Validation du typage via un script de test local `python test_domain.py`.

#### ⚠️ Pièges Fréquents & Conseils
- *Piège :* Étudiants qui passent trop de temps sur le scénario et négligent la modélisation POO.
- *Conseil :* Les cadrer rapidement : le scénario peut être simple (3-4 salles), c'est la qualité des classes Python qui compte.

#### 📌 Critères de Validation
- Script autonome de test instanciant 3 salles du scénario du groupe et validant le passage d'une énigme en POO pure.

---

### 🟢 Séance 2 — Exposition API REST : Navigation Joueur & Validation Pydantic

- **Durée :** 3 h  
- **Module :** M1 — FastAPI, Routing & Pydantic
- **Focus Cyber/Technique :** API REST, verbes HTTP, Query/Path parameters, Pydantic `BaseModel`, validation de types strictes, documentation Swagger OpenAPI.

#### 💬 Brief Client pour le Groupe
> *"Votre client souhaite tester une première version alpha de l'API REST. L'application mobile du Joueur doit pouvoir interroger la liste des salles accessibles, inspecter des objets et soumettre des réponses aux énigmes avec une validation de saisie irréprochable."*

#### ⚙️ Spécifications Backend à développer
- Endpoints REST Joueur :
  - `GET /health` : Statut du moteur de jeu.
  - `GET /rooms` : Liste des salles découvertes par le joueur.
  - `GET /rooms/{room_id}` : Détail d'une salle, objets visibles et verrous.
  - `POST /puzzles/submit` : Tentative de résolution d'une énigme.
- Modèles Pydantic (`schemas/`) :
  - `PuzzleSubmission` (`puzzle_id: str`, `attempt_code: str`, `player_id: str`).
  - Validateurs Pydantic (regex sur les formats de réponse, suppression des espaces inutiles, rejet des chaînes vides).

#### 📋 Déroulé Pédagogique Formateur
1. **Intro (45 min) :** Principes REST, routage FastAPI, typage Pydantic et auto-documentation OpenAPI.
2. **Démo (15 min) :** Manipulation de Swagger UI (`http://127.0.0.1:8000/docs`).
3. **TP en Équipe (1h45) :** Développement des schemas Pydantic et des endpoints de jeu.
4. **Débrief (15 min) :** Démonstration des erreurs 422 déclenchées sur des mauvaises requêtes JSON.

#### ⚠️ Pièges Fréquents & Conseils
- *Piège :* Confondre les paramètres de route Query (`?code=123`) et les corps de requête JSON (`POST body`).
- *Conseil :* Exiger que les soumissions d'énigmes utilisent des verbes `POST` avec un body Pydantic.

#### 📌 Critères de Validation
- Navigation fonctionnelle dans Swagger UI permettant de tester la soumission de réponses d'énigmes validées par Pydantic.

---

### 🟢 Séance 3 — Architecture Clean, Erreurs HTTP & Logs du Game Master

- **Durée :** 3 h  
- **Module :** M2 — Structuration de projet, exceptions et journalisation
- **Focus Cyber/Technique :** APIRouter, séparation par couche, codes de statut HTTP appropriés (400, 403, 404), `HTTPException`, logging applicatif structuré.

#### 💬 Brief Client pour le Groupe
> *"Les Game Masters se plaignent : si un joueur commet une erreur (porte verrouillée, mauvais code), l'API ne renvoie pas les bons codes HTTP. De plus, les Game Masters ont besoin d'un fichier de log structuré (`gamemaster.log`) pour suivre en direct les actions des joueurs pendant une session."*

#### ⚙️ Spécifications Backend à développer
- Structuration modulaire avec `APIRouter` :
  - `app/routers/player_game.py`
  - `app/routers/puzzles.py`
- Exceptions HTTP explicites :
  - `404 Not Found` : Salle ou énigme inexistante.
  - `403 Forbidden` : Tentative d'ouvrir une porte verrouillée sans l'objet requis.
  - `400 Bad Request` : Énigme déjà résolue ou soumission invalide.
- Logging Game Master (`app/core/logging.py`) : Enregistrer dans `gamemaster.log` chaque tentative avec timestamp, IP joueur, action et statut (`SUCCESS` / `FAILED_ATTEMPT`).

#### 📋 Déroulé Pédagogique Formateur
1. **Intro (45 min) :** Avantages d'une clean architecture (`routers/`, `services/`, `schemas/`), sémantique des codes HTTP, module `logging`.
2. **TP en Équipe (1h45) :** Structuration du dépôt et implémentation du système de logs & handlers d'exceptions.
3. **Débrief (30 min) :** Inspection du fichier `gamemaster.log` généré lors des tests.

#### ⚠️ Pièges Fréquents & Conseils
- *Piège :* Renvoyer systématiquement du `500 Internal Server Error` lors d'une mauvaise manipulation du joueur.
- *Conseil :* Rappeler qu'une erreur d'un joueur est un comportement normal de l'application -> Lever une `HTTPException` `4xx`.

#### 📌 Critères de Validation
- La tentative d'accès à une zone interdite retourne un statut HTTP `403` et consigne une ligne dans `gamemaster.log`.

---

### 🟢 Séance 4 — PostgreSQL & SQLAlchemy : Base de Données du Jeu

- **Durée :** 3 h  
- **Module :** M3 — Base de données PostgreSQL & ORM SQLAlchemy
- **Focus Cyber/Technique :** Database relationnelle, connexion SQLAlchemy v2, modèles ORM, injection de dépendance `get_db`, opérations CRUD.

#### 💬 Brief Client pour le Groupe
> *"Actuellement, les parties sont perdues à chaque redémarrage du serveur ! Vous devez raccorder le moteur d'Escape Game à une base PostgreSQL afin de persister la progression des joueurs, l'état des verrous et l'inventaire."*

#### ⚙️ Spécifications Backend à développer
- Connexion PostgreSQL dans `app/database.py`.
- Modèles SQLAlchemy (`app/models/`) :
  - `UserModel` (`id`, `username`, `role`, `created_at`).
  - `RoomModel` (`id`, `name`, `description`, `is_unlocked`).
  - `PuzzleModel` (`id`, `room_id`, `solution_hash`, `is_solved`).
- Service CRUD (`app/services/engine_service.py`) pour lire la position du joueur et mettre à jour l'état des salles en base de données.

#### 📋 Déroulé Pédagogique Formateur
1. **Intro (45 min) :** Modèles ORM vs Schemas Pydantic, session SQLAlchemy, pattern Dependency Injection avec FastAPI (`Depends(get_db)`).
2. **TP en Équipe (2h) :** Écriture des modèles SQL du jeu et des fonctions de persistence.

#### ⚠️ Pièges Fréquents & Conseils
- *Piège :* Confondre les types des colonnes SQLAlchemy et les types Pydantic (ex: `Column(String)` vs `str`).
- *Conseil :* Montrer clairement la coexistence des deux dossiers (`app/models/` et `app/schemas/`).

#### 📌 Critères de Validation
- Redémarrer l'API ne réinitialise plus la partie : la progression du joueur est lue et sauvegardée dans PostgreSQL.

---

### 🟢 Séance 5 — Relations SQL, Alembic & Tests de Recette Pytest

- **Durée :** 3 h  
- **Module :** M3 — Relations SQL, Alembic & Tests automatisés
- **Focus Cyber/Technique :** Clés étrangères (FK), relations One-to-Many / Many-to-Many, Alembic (migrations de schéma), tests `pytest` et `httpx.AsyncClient`.

#### 💬 Brief Client pour le Groupe
> *"DigitalEscape Studio exige un niveau de qualité élevé : le schéma DB doit gérer des relations complexes (Inventaire des joueurs <-> Objets, Salles <-> Portes) et chaque parcours de jeu doit être validé par des tests d'intégration automatisés."*

#### ⚙️ Spécifications Backend à développer
- Modélisation des relations SQLAlchemy :
  - Relation Many-to-Many : `player_inventory` (`user_id`, `item_id`).
  - Relation One-to-Many : `Room` -> `Puzzle`.
- Gestion du schéma avec **Alembic** (`alembic revision --autogenerate -m "Add inventory and relations"`).
- Suite de tests `pytest` (`tests/test_gameplay.py`) :
  - Test de résolution d'une énigme et vérification en DB du changement d'état de la porte.
  - Utilisation d'une base de données SQLite de test isolée.

#### 📋 Déroulé Pédagogique Formateur
1. **Intro (45 min) :** Relations ORM (`relationship`, `back_populates`), commandes Alembic et fixtures `pytest`.
2. **TP en Équipe (1h45) :** Réalisation des migrations et écriture des tests d'intégration.
3. **Débrief (30 min) :** Exécution du runner pytest sur l'ensemble de la classe.

#### ⚠️ Pièges Fréquents & Conseils
- *Piège :* Oublier de faire `alembic upgrade head` avant d'exécuter l'application.
- *Conseil :* Ajouter la commande de migration dans le README du projet.

#### 📌 Critères de Validation
- La commande `pytest` s'exécute avec 100% de réussite sur les scénarios de jeu du groupe.

---

### 🟢 Séance 6 — Authentification JWT : Espace Joueur & Game Master

- **Durée :** 3 h  
- **Module :** M4 — Authentification JWT
- **Focus Cyber/Technique :** Hachage sécurisé de mots de passe (bcrypt/argon2), jetons JSON Web Tokens (JWT), OAuth2PasswordBearer, signature HMAC-SHA256, en-têtes HTTP de sécurité.

#### 💬 Brief Client pour le Groupe
> *"Pour commercialiser le jeu, la plateforme a besoin d'un système d'authentification sécurisé. Joueurs et Game Masters doivent pouvoir créer un compte, se connecter et obtenir un Token JWT pour accéder aux endpoints protégés."*

#### ⚙️ Spécifications Backend à développer
- Endpoints d'authentification (`app/routers/auth.py`) :
  - `POST /auth/register` : Création de compte avec mot de passe haché (`passlib` / `pwd_context`).
  - `POST /auth/login` : Authentification (OAuth2) et génération d'un token JWT signé (valide 1h).
  - `GET /auth/me` : Profil de l'utilisateur connecté via la dépendance `get_current_user`.
- Header d'accès obligatoire : `Authorization: Bearer <TOKEN_JWT>`.

#### 📋 Déroulé Pédagogique Formateur
1. **Intro (45 min) :** Principes du JWT, pourquoi hacher les mots de passe (salage, bcrypt), prévention des attaques sur les tokens.
2. **Live-coding (30 min) :** Implémentation du module `security.py` (création & décodage JWT).
3. **TP en Équipe (1h30) :** Sécurisation des endpoints du jeu avec la dépendance `get_current_user`.

#### ⚠️ Pièges Fréquents & Conseils
- *Piège :* Stocker le mot de passe en texte clair dans la table PostgreSQL.
- *Conseil :* Vérifier immédiatement en DB SQL que la colonne `hashed_password` contient bien des empreintes bcrypt (`$2b$...`).

#### 📌 Critères de Validation
- Se connecter avec `/auth/login` renvoie un JWT valide permettant d'effectuer des actions de jeu en tant que joueur identifié.

---

### 🟢 Séance 7 — Autorisation RBAC, Scopes & Commandes Game Master

- **Durée :** 3 h  
- **Module :** M4 — Autorisation et sécurité API
- **Focus Cyber/Technique :** Role-Based Access Control (RBAC), séparation des privilèges (`player`, `game_master`, `admin`), audit trail, protection contre le dépassement de droits.

#### 💬 Brief Client pour le Groupe
> *"Un simple Joueur ne doit pas pouvoir débloquer une porte à distance ou consulter les logs des autres parties ! Vous devez mettre en place un contrôle d'accès basé sur les rôles (RBAC) pour réserver les fonctions d'administration aux seuls Game Masters."*

#### ⚙️ Spécifications Backend à développer
- Rôles utilisateurs : `ROLE_PLAYER`, `ROLE_GAME_MASTER`, `ROLE_ADMIN`.
- Dépendance de contrôle de rôle : `RequireRole(["ROLE_GAME_MASTER"])`.
- Endpoints exclusifs Game Master (`app/routers/gm_control.py`) :
  - `POST /gm/sessions/{session_id}/override-puzzle` : Force le déverrouillage d'une énigme si des joueurs sont bloqués.
  - `GET /gm/audit-trail` : Consultation des événements d'audit (actions GM et tentatives suspectes).
- Enregistrement automatique dans la table `audit_events`.

#### 📋 Déroulé Pédagogique Formateur
1. **Intro (45 min) :** Modèle RBAC, gestion des autorisations dans FastAPI, traçabilité des opérations sensibles (Audit Log).
2. **TP en Équipe (2h) :** Implémentation de la vérification de rôles et création de l'espace API Game Master.

#### ⚠️ Pièges Fréquents & Conseils
- *Piège :* Permettre à un utilisateur de modifier lui-même son rôle lors du `/auth/register`.
- *Conseil :* Forcer le rôle `ROLE_PLAYER` par défaut lors de l'inscription publique.

#### 📌 Critères de Validation
- Un utilisateur `ROLE_PLAYER` qui tente d'invoquer `/gm/override-puzzle` reçoit un statut `403 Forbidden` immédiat.

---

### 🟢 Séance 8 — Traitements Asynchrones (`async/await`) : Le Défi Multi-Flux

- **Durée :** 3 h  
- **Module :** M5 — Async / Await avec FastAPI
- **Focus Cyber/Technique :** Programmation asynchrone, boucle d'événements (Event Loop), `async/await`, `asyncio.gather`, requêtes I/O non-bloquantes.

#### 💬 Brief Client pour le Groupe
> *"Le cahier des charges impose une 'Énigme Climax' dans votre Escape Game : les joueurs doivent désamorcer ou déverrouiller un mécanisme en interrogeant 4 sous-systèmes simultanés. Si votre backend traite ces requêtes de façon synchrone, la réponse met trop de temps et le délai expire !"*

#### ⚙️ Spécifications Backend à développer
- Module d'énigme complexe asynchrone (`app/services/async_solvers.py`).
- Endpoint `POST /puzzles/climax-override` :
  - Exécution synchrone (anti-pattern) : 4 sous-opérations de 800ms = 3.2s -> **Échec (Timeout de la partie)**.
  - Exécution asynchrone optimisée avec `asyncio.gather()` : Exécution parallèle des 4 vérifications -> **Succès en ~800ms**.
- Utilisation des méthodes asynchrones SQLAlchemy (`AsyncSession`) et `httpx.AsyncClient`.

#### 📋 Déroulé Pédagogique Formateur
1. **Intro (45 min) :** Event Loop Python, quand utiliser `async`, pièges des appels I/O synchrones bloquants, utilisation de `asyncio.gather`.
2. **TP en Équipe (1h45) :** Développement de l'énigme asynchrone et mesure des temps d'exécution (benchmarks).
3. **Débrief (30 min) :** Comparaison des temps de réponse en console.

#### ⚠️ Pièges Fréquents & Conseils
- *Piège :* Utiliser `time.sleep()` dans une fonction `async def`, ce qui bloque tout le serveur web.
- *Conseil :* Insister sur l'utilisation exclusive de `await asyncio.sleep()`.

#### 📌 Critères de Validation
- L'énigme climax répond en moins d'une seconde grâce au traitement parallèle `asyncio.gather`.

---

### 🟢 Séance 9 — Scripting Python & Parsing de Logs (Forensics / Audit GM)

- **Durée :** 3 h  
- **Module :** M6 — Scripting Python & Automatisation
- **Focus Cyber/Technique :** Parsing de fichiers textuels et logs, expressions régulières (Regex `re`), structures de données, extraction d'anomalies.

#### 💬 Brief Client pour le Groupe
> *"Incident de jeu ! Une partie s'est interrompue subitement suite à un crash serveur. Le Game Master ne dispose que d'un fichier de log brut (`session_raw.log`). Vous devez écrire un script Python autonome pour parser ce fichier, reconstruire les actions des joueurs et générer un rapport de secours."*

#### ⚙️ Spécifications Backend & Script à développer
- Fichier log exemple : `data/session_raw.log` (généré avec des requêtes de joueurs, échecs et tentatives de triche).
- Script autonome `scripts/parse_session_logs.py` :
  - Analyse du fichier par expressions régulières (Regex).
  - Identification des tentatives de brute-force (ex: > 20 essais sur un même puzzle).
  - Reconstruction de la chronologie des clés trouvées par l'équipe.
  - Export d'un rapport structuré JSON (`data/session_recovery_report.json`).
- Endpoint API d'ingestion : `POST /gm/ingest-report` pour réimporter les données récupérées dans PostgreSQL.

#### 📋 Déroulé Pédagogique Formateur
1. **Intro (45 min) :** Module `re` (Regex Python), lecture efficace de fichiers avec `with open()`, sérialisation JSON.
2. **TP en Équipe (2h) :** Écriture du script de parsing et validation de l'extraction des événements clés.

#### ⚠️ Pièges Fréquents & Conseils
- *Piège :* Écrire des expressions régulières trop rigides qui plantent à la moindre variation de format de ligne log.
- *Conseil :* Montrer des regex flexibles avec groupes nommés `(?P<name>...)`.

#### 📌 Critères de Validation
- Le script `parse_session_logs.py` extrait correctement la liste des puzzles résolus à partir du fichier log brut.

---

### 🟢 Séance 10 — Console CLI du Game Master (`argparse`)

- **Durée :** 3 h  
- **Module :** M6 — Interface en ligne de commande (CLI)
- **Focus Cyber/Technique :** Outils en ligne de commande (CLI), module `argparse`, sous-commandes, automatisation d'opérations d'administration.

#### 💬 Brief Client pour le Groupe
> *"Les Game Masters en salle de contrôle ont besoin d'une console d'administration ultra-rapide en ligne de commande (`gm-console`) pour surveiller les parties, débloquer un groupe à distance ou consulter l'état d'un serveur sans passer par un navigateur."*

#### ⚙️ Spécifications CLI à développer
- Application CLI dans `cli/gm_console.py`.
- Commandes CLI supportées :
  ```bash
  python -m cli.gm_console login --username gm_alice --password "GMSecret123!"
  python -m cli.gm_console status --session-id 42
  python -m cli.gm_console override --session-id 42 --puzzle-id P-03
  python -m cli.gm_console audit-summary
  ```
- Stockage local sécurisé du jeton JWT Game Master dans un fichier `.gm_session`.
- Affichage clair et structuré des réponses dans le terminal.

#### 📋 Déroulé Pédagogique Formateur
1. **Intro (45 min) :** Construction d'outils CLI avec `argparse` (subparsers, options, arguments positionnels).
2. **TP en Équipe (2h) :** Développement de la console CLI Game Master et connexion aux endpoints de l'API.

#### ⚠️ Pièges Fréquents & Conseils
- *Piège :* Crash brut de la CLI avec Stacktrace Python si l'API FastAPI n'est pas lancée.
- *Conseil :* Intercepter l'erreur de connexion `httpx.ConnectError` et afficher un message amical à l'utilisateur.

#### 📌 Critères de Validation
- Le Game Master peut débloquer une énigme d'une partie en cours directement via sa console CLI.

---

### 🟢 Séance 11 — Consumption d'APIs Tierces : Le Service d'Indices Externe

- **Durée :** 3 h  
- **Module :** M7 — APIs tierces avec `requests` / `httpx`
- **Focus Cyber/Technique :** Appel d'APIs externes HTTP, requêtes sortantes (`httpx`), timeouts, retries, gestion d'erreurs réseaux et fallback.

#### 💬 Brief Client pour le Groupe
> *"DigitalEscape Studio intègre un microservice externe de génération d'indices par IA / Threat Intelligence. Votre moteur d'Escape Game doit interroger ce service tiers lorsqu'un joueur demande un indice ou soumet un hash cryptographique."*

#### ⚙️ Spécifications Backend à développer
- Service d'interrogation externe (`app/services/hint_service.py`).
- Intégration HTTP sortante :
  - `POST /puzzles/{id}/request-hint` : L'API du groupe appelle l'API tierce (ou le serveur Mock du formateur) pour obtenir un indice adapté.
- Gestion des exigences non-fonctionnelles :
  - **Timeout** obligatoire (max 3.0s).
  - Mode dégradé (Fallback) : Si l'API tierce est injoignable, retourner un indice par défaut pré-enregistré en DB local.

#### 📋 Déroulé Pédagogique Formateur
1. **Intro (45 min) :** Utilisation de `httpx.AsyncClient` pour les requêtes sortantes, gestion des timeouts et stratégies de fallback.
2. **TP en Équipe (1h45) :** Implémentation du service d'indices et intégration dans l'API du jeu.
3. **Débrief (30 min) :** Simulation d'une panne du service tiers pour valider le mode dégradé.

#### ⚠️ Pièges Fréquents & Conseils
- *Piège :* Oublier de mettre un `timeout` sur les requêtes sortantes `httpx`.
- *Conseil :* Faire de la gestion des timeouts un critère obligatoire de validation.

#### 📌 Critères de Validation
- La demande d'indice fait bien appel au service distant et bascule proprement sur un indice local en cas d'interruption du réseau.

---

### 🟢 Séance 12 — Finalisation, Recette Client & Démo (Soutenance)

- **Durée :** 3 h  
- **Module :** M8 — Finalisation, tests, démo et évaluation
- **Focus Cyber/Technique :** Intégration globale, revue de code, recette applicative, documentation README/Swagger, démonstrations en équipe.

#### 💬 Brief Client pour le Groupe
> *"Jour de livraison finale chez DigitalEscape Studio ! Chaque équipe dispose de 15 minutes pour présenter son projet, faire une démonstration complète du jeu (Joueur & Game Master), et prouver la solidité technique de son API devant le client."*

#### ⚙️ Déroulé de la Recette Finale
1. **Validation de la suite de tests `pytest` (100% Succès).**
2. **Démonstration "Live" par l'équipe (15 min par groupe) :**
   - Présentation de la thématique choisie et de l'architecture backend.
   - Parcours Joueur : Inscription, Auth JWT, Exploration, Soumission d'énigmes, Énigme Async Climax.
   - Parcours Game Master : Supervision, Override d'énigme via la console CLI, consultation de l'audit trail.
3. **Revue du code & Questions du Formateur.**

---

## 📊 Grille d'Évaluation du Projet Fil Rouge (30 Points)

Le formateur évalue le projet livré par chaque équipe à la séance 12 selon la grille suivante :

| Critère d'Évaluation | Notions Pédagogiques Evaluées | Barème |
| :--- | :--- | :---: |
| **1. Conception & Qualité du Code** | Architecture propre (`routers`, `services`, `schemas`), typage Python, originalité de la thématique. | **/ 4 pts** |
| **2. API REST & Validation Pydantic** | Routes REST cohérentes, sémantique des verbes HTTP, validation stricts par Pydantic. | **/ 4 pts** |
| **3. Base de Données PostgreSQL & ORM** | Modèles SQLAlchemy relationnels propres, migrations Alembic et persistance effective. | **/ 4 pts** |
| **4. Sécurité, Auth JWT & RBAC** | Hashage bcrypt des mots de passe, tokens JWT Bearer, séparation stricte des rôles `player` / `game_master`. | **/ 5 pts** |
| **5. Traitements Asynchrones (`async`)** | Utilisation conforme de `async/await` et `asyncio.gather` sur l'énigme climax. | **/ 3 pts** |
| **6. Scripting & Console CLI Game Master** | Script de parsing de logs fonctionnel et console CLI `argparse` Game Master ergonomique. | **/ 4 pts** |
| **7. API Tierce & Mode Dégradé** | Appel HTTP externe avec timeout et gestion propre du fallback. | **/ 3 pts** |
| **8. Tests & Documentation** | Tests `pytest` automatisés et README / documentation Swagger OpenAPI complète. | **/ 3 pts** |
| **TOTAL GENERAL** | **Compétences Backend & FastAPI validées** | **/ 30 pts** |

---

## 🎒 Ressources à Préparer par le Formateur

1. **Dépôt Starter Git** : Proposer une trame minimale avec le découpage des dossiers (`app/`, `tests/`, `scripts/`, `cli/`).
2. **Fichier Log Exemple** : Fichier `session_raw.log` à fournir pour le TP de parsing de logs (Séance 9).
3. **Mock d'API d'Indices Tierce** : Petit script ou endpoint FastAPI léger simulant l'API externe (Séance 11).
