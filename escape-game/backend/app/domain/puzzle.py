"""Puzzle — Classe abstraite polymorphe pour les énigmes.

Deux déclinaisons concrètes sont fournies :

* :class:`CodePuzzle` — compare directement la tentative du joueur avec un
  code secret stocké en clair (cas pédagogique simple).

* :class:`HashPuzzle` — stocke l'empreinte SHA-256 du code secret, jamais le
  code lui-même. C'est le pattern de sécurité utilisé en production pour les
  mots de passe : on ne stocke que le hash, et on vérifie une tentative en
  calculant son hash puis en le comparant au hash attendu.

Le polymorphisme permet au `GameState` et aux routes FastAPI de manipuler des
``Puzzle`` sans se soucier de leur type concret : un simple appel à
``check_solution(answer)`` fait le travail.
"""

from __future__ import annotations

import hashlib
import hmac
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from app.domain.game_element import GameElement


@dataclass
class Puzzle(GameElement, ABC):
    """Classe abstraite de tous les puzzles.

    Toute sous-classe doit implémenter :meth:`check_solution`.
    """

    reward_message: str = "Puzzle résolu !"

    @abstractmethod
    def check_solution(self, answer: str) -> bool:
        """Vérifie si la tentative `answer` est correcte.

        Args:
            answer: Tentative du joueur (texte, code numérique, mot de passe...).

        Returns:
            True si la réponse est correcte, False sinon.
        """
        raise NotImplementedError

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["reward_message"] = self.reward_message
        # On n'expose jamais la solution (ni le code, ni le hash) via l'API.
        data["solution_exposed"] = False
        return data


@dataclass
class CodePuzzle(Puzzle):
    """Puzzle à code en clair.

    La comparaison est directe : ``answer == self.secret_code``.
    Ce type de puzzle est simple mais peu sûr : le code secret est stocké
    en clair en mémoire. À réserver aux énigmes non sensibles.
    """

    secret_code: str = ""

    def check_solution(self, answer: str) -> bool:
        return answer == self.secret_code

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["puzzle_kind"] = "code"
        return data


@dataclass
class HashPuzzle(Puzzle):
    """Puzzle à empreinte cryptographique (sécurisé).

    Le code secret n'est JAMAIS stocké en clair. On stocke uniquement son
    empreinte SHA-256 (`expected_hash`). Lors d'une tentative, on calcule
    le SHA-256 de la réponse du joueur et on le compare au hash attendu.

    Avantages :
        * Si la base de données fuite, l'attaquant ne récupère que des hashes
          impossibles à inverser (sauf attaque par force brute ou dictionnaire).
        * Le Game Master lui-même peut configurer un puzzle sans connaître le
          mot de passe, à partir du moment où il dispose du hash.

    Exemple de hash SHA-256 du mot ``"password"`` :
        ``5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8``
    """

    expected_hash: str = ""
    hash_algorithm: str = field(default="sha256", repr=False)

    @staticmethod
    def compute_hash(answer: str, algorithm: str = "sha256") -> str:
        """Calcule l'empreinte d'une chaîne.

        Args:
            answer: Chaîne à hasher.
            algorithm: Algorithme hashlib supporté ("sha256", "md5", "sha1"...).

        Returns:
            Représentation hexadécimale du hash.
        """
        h = hashlib.new(algorithm)
        h.update(answer.encode("utf-8"))
        return h.hexdigest()

    @classmethod
    def from_plaintext(
        cls,
        *,
        id: str,
        name: str,
        description: str,
        plaintext: str,
        reward_message: str = "Puzzle résolu !",
        algorithm: str = "sha256",
    ) -> "HashPuzzle":
        """Factory pratique : crée un HashPuzzle à partir d'un mot de passe en clair.

        Utile pour initialiser le scénario sans calculer le hash à la main.
        En production, on éviterait même cette méthode et on passerait
        directement le hash fourni par l'administrateur.
        """
        return cls(
            id=id,
            name=name,
            description=description,
            reward_message=reward_message,
            expected_hash=cls.compute_hash(plaintext, algorithm),
            hash_algorithm=algorithm,
        )

    def check_solution(self, answer: str) -> bool:
        if not self.expected_hash:
            return False
        attempt_hash = self.compute_hash(answer, self.hash_algorithm)
        # Comparaison à temps constant pour éviter les attaques par timing.
        return hmac.compare_digest(attempt_hash, self.expected_hash)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["puzzle_kind"] = "hash"
        data["hash_algorithm"] = self.hash_algorithm
        return data
