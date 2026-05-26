# Criar sala, entrar em sala, sair da sala.
from fastapi import APIRouter, Body, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.schemas.player import PlayerRoom
from backend.app.schemas.room import StartRoomRequest
from backend.app.services.room_service import create_room, join_room, start_game

router_room = APIRouter()
templates = Jinja2Templates(directory='templates')

@router_room.post("/rooms")
async def post_room(data : PlayerRoom):
    return create_room(host_player_id=data.host_id)

@router_room.post("/rooms/{room_code}/join")
async def join_room_route(room_code: str, data: dict = Body(...)):
    return join_room(
        player_id=data["player_id"],
        room_code=room_code
    )

@router_room.post("/rooms/{room_id}/start")
async def start_game_route(
    room_id: str,
    data:StartRoomRequest,
    db: Session = Depends(get_db)
):
    return start_game(db, room_id, data.player_id)

