#!/bin/bash

# Création des répertoires
mkdir -p models routers services

# Création des fichiers à la racine
touch __init__.py main.py

# Création des fichiers dans le dossier models
touch models/__init__.py models/player.py

# Création des fichiers dans le dossier routers
touch routers/__init__.py routers/players.py

# Création des fichiers dans le dossier services
touch services/__init__.py services/player_service.py

echo "Structure de dossiers et fichiers créée avec succès !"