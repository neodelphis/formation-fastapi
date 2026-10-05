"""Router de gestion des joueurs (CRUD léger).

Démontre tous les types de routes REST associées aux joueurs :
  * GET    /players          — liste des joueurs
  * GET    /players/{id}     — détail d'un joueur
  * POST   /players          — création d'un joueur
  * PUT    /players/{id}     — mise à jour complète
  * PATCH  /players/{id}     — mise à jour partielle
  * DELETE /players/{id}     — suppression
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.domain.game_state import GameState
from app.domain.player import Player
from app.schemas.player import PlayerCreate, PlayerOut
from app.services.game_engine import get_game_state

router = APIRouter(prefix="/players", tags=["players"])


def _player_to_out(player: Player) -> PlayerOut:
    return PlayerOut(**player.to_dict())


@router.get("", response_model=list[PlayerOut])
def list_players(state: GameState = Depends(get_game_state)) -> list[PlayerOut]:
    """Liste tous les joueurs enregistrés."""
    return [_player_to_out(p) for p in state.list_players()]


@router.get("/{player_id}", response_model=PlayerOut)
def get_player(
    player_id: str, state: GameState = Depends(get_game_state)
) -> PlayerOut:
    """Récupère le détail d'un joueur par son identifiant."""
    player = state.get_player(player_id)
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Joueur introuvable : {player_id}",
        )
    return _player_to_out(player)


@router.post("", response_model=PlayerOut, status_code=status.HTTP_201_CREATED)
def create_player(
    payload: PlayerCreate, state: GameState = Depends(get_game_state)
) -> PlayerOut:
    """Crée un nouveau joueur."""
    if state.get_player(payload.id) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Un joueur avec l'id '{payload.id}' existe déjà.",
        )
    player = Player(
        id=payload.id,
        name=payload.name,
        description=payload.description,
    )
    state.add_player(player)
    return _player_to_out(player)


@router.put("/{player_id}", response_model=PlayerOut)
def update_player(
    player_id: str,
    payload: PlayerCreate,
    state: GameState = Depends(get_game_state),
) -> PlayerOut:
    """Met à jour (remplacement complet) un joueur existant."""
    player = state.get_player(player_id)
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Joueur introuvable : {player_id}",
        )
    player.name = payload.name
    player.description = payload.description
    return _player_to_out(player)


@router.patch("/{player_id}", response_model=PlayerOut)
def patch_player(
    player_id: str,
    payload: dict,
    state: GameState = Depends(get_game_state),
) -> PlayerOut:
    """Met à jour partiellement un joueur (name et/ou description)."""
    player = state.get_player(player_id)
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Joueur introuvable : {player_id}",
        )
    if "name" in payload:
        if not str(payload["name"]).strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Le nom ne peut pas être vide.",
            )
        player.name = payload["name"]
    if "description" in payload:
        player.description = payload["description"]
    return _player_to_out(player)


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(
    player_id: str, state: GameState = Depends(get_game_state)
) -> Response:
    """Supprime un joueur."""
    if not state.remove_player(player_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Joueur introuvable : {player_id}",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
