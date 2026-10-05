"""GameElement — Classe mère de tous les éléments du jeu.

Tous les objets manipulés par le moteur (items, portes, puzzles, salles)
héritent de cette classe de base afin de partager :
  * un identifiant unique (`id`)
  * un nom affichable (`name`)
  * une description narrative (`description`)
  * une méthode `to_dict()` pour la sérialisation JSON.

Cette classe abstraite illustre le principe d'héritage en POO : elle factorise
les attributs communs et impose un contrat (méthode `to_dict`) à toutes ses
sous-classes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GameElement:
    """Classe de base abstraite de tous les éléments du jeu.

    Attributes:
        id: Identifiant unique et stable de l'élément (ex: "room-1", "item-key").
        name: Nom court affichable dans l'interface utilisateur.
        description: Description narrative immersive pour le joueur.
    """

    id: str
    name: str
    description: str

    def to_dict(self) -> dict:
        """Sérialise l'élément en dictionnaire JSON-compatible.

        Returns:
            Dict contenant au minimum `id`, `name` et `description`.
            Les sous-classes doivent étendre ce dictionnaire avec leurs
            attributs spécifiques.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__.lower(),
        }
