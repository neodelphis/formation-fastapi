"""Schemas Pydantic — Contrats d'API entrants et sortants.

Ces modèles ne sont PAS les classes métier : ils servent uniquement à valider
et sérialiser les échanges HTTP. La séparation `domain` (POO pure) / `schemas`
(Pydantic) permet de garder le domaine testable sans dépendance web.
"""
