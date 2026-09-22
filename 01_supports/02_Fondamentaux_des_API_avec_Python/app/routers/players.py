from fastapi import APIRouter, HTTPException

from app.models.player import Player, PlayerCreate
from app.services import player_service


router = APIRouter(
    prefix='/players',
    tags=['players'],
)


@router.get('', response_model=list[Player])
def list_players() -> list[Player]:
    return player_service.get_players()


@router.get('/{player_id}', response_model=Player)
def get_player(player_id: int) -> Player:
    player = player_service.get_player(player_id)

    if player is None:
        raise HTTPException(
            status_code=404,
            detail='Player not found',
        )

    return player


@router.post(
    '',
    response_model=Player,
    status_code=201,
)
def create_player(player: PlayerCreate) -> Player:
    return player_service.create_player(player)


@router.put(
    '/{player_id}',
    response_model=Player,
)
def update_player(
    player_id: int,
    player: PlayerCreate,
) -> Player:
    updated_player = player_service.update_player(
        player_id,
        player,
    )

    if updated_player is None:
        raise HTTPException(
            status_code=404,
            detail='Player not found',
        )

    return updated_player


@router.delete('/{player_id}')
def delete_player(player_id: int) -> dict:
    deleted_player = player_service.delete_player(
        player_id
    )

    if deleted_player is None:
        raise HTTPException(
            status_code=404,
            detail='Player not found',
        )

    return {
        'message': 'Player deleted',
        'player': deleted_player,
    }