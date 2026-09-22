import logging

from app.models.player import Player, PlayerCreate


logger = logging.getLogger(__name__)


players = [
    Player(
        id=1,
        name='Alice',
        score=1200,
        level=12,
    ),
    Player(
        id=2,
        name='Bob',
        score=950,
        level=9,
    ),
    Player(
        id=42,
        name='Zelda',
        score=3000,
        level=99,
    ),
]


next_player_id = max(
    player.id for player in players
) + 1


def get_players() -> list[Player]:
    logger.info('Retrieving all players')
    return players


def get_player(player_id: int) -> Player | None:
    logger.info(
        'Searching for player %s',
        player_id,
    )

    for player in players:
        if player.id == player_id:
            logger.info(
                'Player %s found',
                player_id,
            )
            return player

    logger.warning(
        'Player %s not found',
        player_id,
    )

    return None


def create_player(player_data: PlayerCreate) -> Player:
    global next_player_id

    player = Player(
        id=next_player_id,
        **player_data.model_dump(),
    )

    players.append(player)

    logger.info(
        'Player %s created',
        player.id,
    )

    next_player_id += 1

    return player


def update_player(
    player_id: int,
    player_data: PlayerCreate,
) -> Player | None:
    for index, player in enumerate(players):
        if player.id == player_id:
            updated_player = Player(
                id=player_id,
                **player_data.model_dump(),
            )

            players[index] = updated_player

            logger.info(
                'Player %s updated',
                player_id,
            )

            return updated_player

    logger.warning(
        'Player %s not found for update',
        player_id,
    )

    return None


def delete_player(player_id: int) -> Player | None:
    for index, player in enumerate(players):
        if player.id == player_id:
            deleted_player = players.pop(index)

            logger.info(
                'Player %s deleted',
                player_id,
            )

            return deleted_player

    logger.warning(
        'Player %s not found for deletion',
        player_id,
    )

    return None