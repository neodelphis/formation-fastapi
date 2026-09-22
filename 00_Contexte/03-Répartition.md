# Vue globale du cours sur 36 heures

## Répartition horaire globale

| Module    |                                        Thématique |    Durée |
| --------- | ------------------------------------------------: | -------: |
| M0        |  Environnement, révision POO appliquée au backend |      3 h |
| M1        | FastAPI, routing, Pydantic, documentation OpenAPI |      6 h |
| M2        | Structuration projet, erreurs, logging, debugging |      3 h |
| M3        |                        Base de données PostgreSQL |      6 h |
| M4        |  Authentification JWT, autorisation, sécurité API |      6 h |
| M5        |         Programmation asynchrone avec async/await |      3 h |
| M6        |            Scripting Python pour la cybersécurité |      6 h |
| M7        |              Interaction avec APIs tierces et CLI |      6 h |
| M8        |             Finalisation, tests, démo, évaluation |      3 h |
| **Total** |                                                   | **36 h** |

## Tableau synthétique des séances

| Séance | Durée | Thème principal                   | Lien cybersécurité                             |
| -----: | ----: | --------------------------------- | ---------------------------------------------- |
|      1 |   3 h | POO, environnement, bases Python  | Modélisation d’alertes, actifs, vulnérabilités |
|      2 |   3 h | FastAPI, routing, Pydantic        | API d’alertes avec validation sécurité         |
|      3 |   3 h | Structuration, erreurs, logging   | Journalisation d’événements et audit           |
|      4 |   3 h | PostgreSQL, SQLAlchemy            | Persistance des actifs et alertes              |
|      5 |   3 h | Relations, migrations, tests      | Jeu de données SOC, tests de validation        |
|      6 |   3 h | Authentification JWT              | Login sécurisé, tokens, hash de mots de passe  |
|      7 |   3 h | Autorisation, rôles, sécurité API | RBAC analyst/admin/viewer, audit               |
|      8 |   3 h | Async/await                       | Enrichissement concurrent d’IOC                |
|      9 |   3 h | Scripting, parsing                | Analyse de logs SSH/firewall/web               |
|     10 |   3 h | CLI argparse                      | Outils d’import, export, reporting             |
|     11 |   3 h | APIs tierces                      | Threat intelligence, enrichissement IP/hash    |
|     12 |   3 h | Finalisation, évaluation          | Démo complète du SOC API                       |

# Version condensée du plan


## Module Python Backend & FastAPI — 36 h

### Séance 1 — Python, POO et environnement backend
Révision des classes, héritage, polymorphisme. Modélisation d’objets cybersécurité : actifs, alertes, vulnérabilités.

### Séance 2 — FastAPI et Pydantic
Création d’une API REST, routing, validation, documentation Swagger.

### Séance 3 — Structuration, erreurs et logging
Organisation routes/services/modèles, gestion des erreurs HTTP, logs, debugging.

### Séance 4 — PostgreSQL avec SQLAlchemy
Connexion à PostgreSQL, modèles persistants, premiers CRUD.

### Séance 5 — Relations, migrations et tests
Relations entre tables, Alembic, données de démonstration, tests pytest.

### Séance 6 — Authentification JWT
Inscription, login, hash des mots de passe, génération et validation de tokens.

### Séance 7 — Autorisation et sécurité API
Rôles, permissions, audit, bonnes pratiques sécurité API.

### Séance 8 — Async/await
Endpoints asynchrones, concurrence, enrichissement parallèle d’indicateurs.

### Séance 9 — Scripting et parsing de logs
Analyse de fichiers logs, extraction d’IP, détection de comportements suspects.

### Séance 10 — CLI avec argparse
Industrialisation des scripts, sous-commandes, rapport et automatisation.

### Séance 11 — APIs tierces avec requests/httpx
Consommation d’APIs externes, authentification, timeouts, enrichissement threat intel.

### Séance 12 — Finalisation et évaluation
Tests, documentation, revue de code, démonstration du projet SecureSOC API.

