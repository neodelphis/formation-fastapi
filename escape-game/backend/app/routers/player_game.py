"""Router d'exploration du jeu — salles, items, puzzles.

C'est le cœur de l'API "joueur" : explorer les salles, ramasser des items,
et tenter de résoudre des puzzles.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.domain.game_state import GameState
from app.schemas.puzzle import PuzzleSubmission, PuzzleSubmissionResult
from app.schemas.room import RoomOut, RoomSummary
from app.services.game_engine import get_game_state

router = APIRouter(tags=["exploration"])


@router.get("/rooms", response_model=list[RoomSummary])
def list_rooms(state: GameState = Depends(get_game_state)) -> list[RoomSummary]:
    """Liste les salles du scénario (vue résumée, sans le détail des items)."""
    summaries: list[RoomSummary] = []
    for room in state.list_rooms():
        summaries.append(
            RoomSummary(
                id=room.id,
                name=room.name,
                description=room.description,
                is_start=room.is_start,
                is_exit=room.is_exit,
                items_count=len(room.items),
                puzzles_count=len(room.puzzles),
            )
        )
    return summaries


@router.get("/rooms/{room_id}", response_model=RoomOut)
def get_room(room_id: str, state: GameState = Depends(get_game_state)) -> RoomOut:
    """Retourne le détail d'une salle (items, portes, puzzles)."""
    room = state.get_room(room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salle introuvable : {room_id}",
        )
    return RoomOut(**room.to_dict())


@router.post("/puzzles/submit", response_model=PuzzleSubmissionResult)
def submit_puzzle(
    payload: PuzzleSubmission, state: GameState = Depends(get_game_state)
) -> PuzzleSubmissionResult:
    """Vérifie une tentative de résolution de puzzle.

    Le corps de requête est validé par Pydantic via `PuzzleSubmission` :
    si `attempt_code` est vide ou composé d'espaces, Pydantic lèvera une
    `ValueError` qui sera automatiquement convertie en HTTP 422
    Unprocessable Entity par FastAPI.
    """
    result = state.submit_puzzle(
        player_id=payload.player_id,
        puzzle_id=payload.puzzle_id,
        attempt_code=payload.attempt_code,
    )
    if not result.success and result.message.startswith("Joueur inconnu"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result.message
        )
    if not result.success and result.message.startswith("Puzzle introuvable"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=result.message
        )
    return PuzzleSubmissionResult(
        success=result.success,
        message=result.message,
        unlocked_door_id=result.unlocked_door_id,
        reward_item_ids=result.reward_item_ids,
    )


@router.post("/players/{player_id}/move/{room_id}")
def move_player(
    player_id: str,
    room_id: str,
    state: GameState = Depends(get_game_state),
) -> dict:
    """Déplace un joueur vers une salle."""
    player = state.move_player(player_id, room_id)
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Joueur ou salle introuvable.",
        )
    return {"success": True, "current_room_id": player.current_room_id}


@router.post("/players/{player_id}/pickup/{item_id}")
def pickup_item(
    player_id: str,
    item_id: str,
    state: GameState = Depends(get_game_state),
) -> dict:
    """Ramasse un item présent dans la salle courante du joueur."""
    player = state.pickup_item(player_id, item_id)
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Joueur introuvable, salle courante invalide, ou item absent.",
        )
    return {"success": True, "inventory": player.inventory}
