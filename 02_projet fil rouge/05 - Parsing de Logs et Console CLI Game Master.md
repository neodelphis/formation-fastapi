# 🚀 05 — Scripting Forensics & Console CLI Game Master

- **Séances couvertes :** Séance 9 & Séance 10
- **Objectifs de la journée :**
  - Écrire un script Python autonome d'analyse forensics de logs bruts à l'aide des expressions régulières (Regex).
  - Développer une interface en ligne de commande (CLI) avec `argparse` pour permettre aux Game Masters de piloter le jeu depuis leur terminal.

---

## 💼 Brief Client : Mission "DigitalEscape Studio"

> *"Deux nouveaux besoins d'outils d'automatisation ! Tout d'abord, en cas d'interruption de réseau, les Game Masters doivent pouvoir parser un fichier log brut de partie (`session_raw.log`) pour reconstituer l'historique des énigmes résolues par un groupe. Ensuite, les Game Masters en salle de contrôle exigent un outil CLI rapide (`gm-console`) pour administrer le jeu directement depuis leur terminal texte sans passer par le navigateur."*

---

## 🧩 Partie 1 : Scripting Forensics & Parsing de Logs (`scripts/`)

### 🧠 Notions Théoriques Clés
- **Expressions Régulières (`re`)** : Extraction de motifs complexes dans du texte.
- **Manipulation de Fichiers (`with open()`)** : Lecture efficace ligne par ligne sans tout charger en RAM.

### 🎯 Travail à Réaliser en Équipe

#### Étape 1.1 : Le Fichier Log à Parser (`data/session_raw.log`)
Le formateur met à votre disposition un fichier log contenant des centaines de lignes d'événements.

#### Étape 1.2 : Rédaction du Script (`scripts/parse_session_logs.py`)
Écrivez un script autonome pour :
1. Lire `data/session_raw.log` ligne par ligne.
2. Utiliser des Regex pour extraire :
   - Les tentatives de brute-force (> 10 échecs consécutifs sur la même énigme).
   - La liste exacte des puzzles valablement résolus.
   - Les horodatages de chaque résolution.
3. Exporter le résultat dans un fichier JSON `data/session_recovery_report.json`.

Exemple de Regex :
```python
import re

pattern = re.compile(r"\[(?P<timestamp>.*?)\] - USER:(?P<user>\w+) - ACTION:(?P<action>\w+) - PUZZLE:(?P<puzzle_id>\w+) - RESULT:(?P<result>\w+)")
```

#### Étape 1.3 : Réintégration dans l'API
Ajoutez un endpoint Game Master `POST /gm/ingest-report` pour injecter automatiquement le rapport JSON extrait dans la base de données PostgreSQL.

---

## 🧩 Partie 2 : Console CLI Game Master (`cli/gm_console.py`)

### 🧠 Notions Théoriques Clés
- **Module `argparse`** : Parser d'arguments de ligne de commande standard en Python.
- **Subparsers** : Sous-commandes CLI (ex: `git commit`, `docker run`).
- **Requêtes HTTP CLI (`httpx`)** : Interagir avec l'API depuis la console Python.

### 🎯 Travail à Réaliser en Équipe

#### Étape 2.1 : Structure de la Console CLI (`cli/gm_console.py`)
Créez la CLI d'administration avec `argparse` :

```python
import argparse
import httpx

def main():
    parser = argparse.ArgumentParser(description="Console Game Master - EscapeEngine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Commande Login
    login_parser = subparsers.add_parser("login", help="Connexion Game Master")
    login_parser.add_argument("--username", required=True)
    login_parser.add_argument("--password", required=True)

    # Commande Status
    status_parser = subparsers.add_parser("status", help="Statut du serveur de jeu")

    # Commande Override
    override_parser = subparsers.add_parser("override", help="Débloquer une énigme à distance")
    override_parser.add_argument("--puzzle-id", required=True)

    args = parser.parse_args()
    # Logique d'exécution des requêtes HTTP sortantes...

if __name__ == "__main__":
    main()
```

#### Étape 2.2 : Gestion de la Session JWT Locale
Lorsque le Game Master exécute `python -m cli.gm_console login`, enregistrez le jeton JWT renvoyé par l'API dans un fichier temporaire caché `.gm_session`. Les commandes suivantes (`override`, `status`) utiliseront automatiquement ce jeton !

---

## 🏁 Checklist de fin de TP

- [ ] Le script `parse_session_logs.py` s'exécute sans erreur et génère le fichier `session_recovery_report.json`.
- [ ] La console CLI permet à un Game Master de se connecter (`python -m cli.gm_console login ...`).
- [ ] Le Game Master peut débloquer une énigme à distance en exécutant la commande CLI `python -m cli.gm_console override --puzzle-id P-101`. 🖥️
