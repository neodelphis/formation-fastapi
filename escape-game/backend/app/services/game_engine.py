"""Game Engine — Service qui initialise le scénario cyberpunk et expose le GameState.

Le scénario "Operation: Neon Cyberpunk" comporte 3 salles :
  1. `server-room`    — Salle des serveurs (point de départ)
  2. `security-hub`   — Hub de sécurité (porte verrouillée par HashPuzzle)
  3. `mainframe-core` — Cœur du mainframe (sortie / victoire, CodePuzzle final)

Le singleton `game_state` est partagé entre toutes les requêtes HTTP.
"""

from __future__ import annotations

from app.domain.door import Door
from app.domain.game_state import GameState
from app.domain.item import Item
from app.domain.puzzle import CodePuzzle, HashPuzzle
from app.domain.player import Player
from app.domain.room import Room

GAME_TITLE = "Operation: Neon Cyberpunk"
GAME_MASTER = "IA-Sentinel"
ENGINE_VERSION = "1.0.0"


def build_scenario() -> GameState:
    """Construit le scénario cyberpunk initial et retourne un GameState prêt à l'emploi."""
    state = GameState()

    # ------------------------------------------------------------------ #
    # Salle 1 : Server Room (point de départ)
    # ------------------------------------------------------------------ #
    server_room = Room(
        id="server-room",
        name="Salle des Serveurs",
        description=(
            "Un bourdonnement sourd emplit la pièce. Des baies de serveurs "
            "clignotent à l'unisson, projetant des éclats bleus sur les murs "
            "métalliques. Une note jaune est collée sur l'un des panneaux."
        ),
        is_start=True,
    )

    # Items
    note = Item(
        id="item-sticky-note",
        name="Post-it jaune",
        description=(
            "Un post-it griffonné à la hâte : 'Le mot de passe du hub de "
            "sécurité est : neon2099. Ne le laisse traîner nulle part !'"
        ),
    )
    badge = Item(
        id="item-access-badge",
        name="Badge d'accès",
        description="Un badge RFID niveau 2. Peut ouvrir certaines portes.",
        usable=True,
    )
    server_room.items.extend([note, badge])

    # Porte vers le security-hub
    door_to_hub = Door(
        id="door-hub",
        name="Porte blindée vers le Hub",
        description="Une porte blindée marquée 'SECURITY HUB — RESTRICTED'.",
        is_locked=False,
        target_room_id="security-hub",
    )
    server_room.doors.append(door_to_hub)

    # ------------------------------------------------------------------ #
    # Salle 2 : Security Hub (porte verrouillée par HashPuzzle)
    # ------------------------------------------------------------------ #
    security_hub = Room(
        id="security-hub",
        name="Hub de Sécurité",
        description=(
            "Des écrans holographiques projettent des schémas de surveillance. "
            "Un terminal sécurisé réclame un mot de passe. Au fond, une porte "
            "renforcée mène au cœur du mainframe."
        ),
    )

    terminal = Item(
        id="item-terminal",
        name="Terminal de sécurité",
        description=(
            "Un terminal verrouillé. L'écran affiche : 'Saisissez le mot de "
            "passe.' Un voyant rouge clignote."
        ),
        usable=True,
    )
    security_hub.items.append(terminal)

    # HashPuzzle : le mot de passe "neon2099" est stocké sous forme de hash SHA-256.
    # La factory `from_plaintext` calcule le hash pour nous à l'initialisation,
    # mais en production on fournirait directement le hash sans jamais connaître
    # le mot de passe en clair.
    hub_puzzle = HashPuzzle.from_plaintext(
        id="puzzle-hub-password",
        name="Mot de passe du Hub",
        description=(
            "Le terminal réclame le mot de passe d'accès au hub de sécurité. "
            "L'IA Sentinel surveille chaque tentative."
        ),
        plaintext="neon2099",
        reward_message="Accès autorisé. Le terminal s'allume en vert.",
    )
    security_hub.puzzles.append(hub_puzzle)

    # Porte verrouillée vers le mainframe-core
    door_to_core = Door(
        id="door-core",
        name="Porte renforcée du Mainframe",
        description="Une porte épaisse marquée 'MAINFRAME CORE'.",
        is_locked=True,
        required_item_id=None,  # s'ouvre via le puzzle
        target_room_id="mainframe-core",
    )
    security_hub.doors.append(door_to_core)

    # ------------------------------------------------------------------ #
    # Salle 3 : Mainframe Core (sortie / victoire)
    # ------------------------------------------------------------------ #
    mainframe_core = Room(
        id="mainframe-core",
        name="Cœur du Mainframe",
        description=(
            "Le cœur pulsant du mainframe. Une lumière rouge baigne la salle. "
            "Un dernier terminal attend un code d'auto-destruction pour "
            "libérer le réseau de l'emprise de l'IA Sentinel."
        ),
        is_exit=True,
    )

    final_puzzle = CodePuzzle(
        id="puzzle-final-code",
        name="Code d'auto-destruction",
        description=(
            "Le terminal affiche : 'CODE D'AUTO-DESTRUCTION REQUIS (4 chiffres)'. "
            "Un indice sur le mur indique : 'Année du bug Y2K.'"
        ),
        secret_code="2000",
        reward_message="Auto-destruction lancée ! L'IA Sentinel s'effondre.",
    )
    mainframe_core.puzzles.append(final_puzzle)

    # ------------------------------------------------------------------ #
    # Enregistrement des salles + liens puzzle -> porte
    # ------------------------------------------------------------------ #
    state.register_room(server_room)
    state.register_room(security_hub)
    state.register_room(mainframe_core)

    # Résoudre puzzle-hub-password déverrouille door-core
    state.link_puzzle_to_door("puzzle-hub-password", "door-core")
    state.link_puzzle_to_rewards("puzzle-hub-password", ["item-master-key"])

    # ------------------------------------------------------------------ #
    # Joueur par défaut (démo)
    # ------------------------------------------------------------------ #
    default_player = Player(
        id="player-1",
        name="Hack3rGhost",
        description="Opératif cybernétique freelance.",
    )
    default_player.visit("server-room")
    state.add_player(default_player)

    return state


# Singleton global partagé entre toutes les requêtes HTTP.
game_state: GameState = build_scenario()


def get_game_state() -> GameState:
    """Dépendance FastAPI utilisée par les routers pour accéder au GameState."""
    return game_state
