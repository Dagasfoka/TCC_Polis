# Criar sala, entrar em sala, sair da sala.
from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.db.redis import redis_client
from backend.app.schemas.redis.player import PlayerRoom
from backend.app.schemas.redis.room import (
    StartRoomRequest,
    JoinRoomRequest,
    PutReady,
    DeletePlayer,
)
from backend.app.services.redis.room_service import (
    create_room,
    join_room,
    start_game,
    put_ready,
    delete_player,
    get_room,
)

router_room = APIRouter()
templates = Jinja2Templates(directory="templates")


@router_room.get("/rooms/{room_code}")
def get_room_route(room_code: str):
    return get_room(room_code)


@router_room.post("/rooms")
def post_room(data: PlayerRoom):
    return create_room(host_player_id=data.host_id)


@router_room.post("/rooms/{room_code}/join")
async def join_room_route(room_code: str, data: JoinRoomRequest):
    return join_room(
        player_id=data.player_id,
        room_code=room_code,
    )


@router_room.post("/rooms/{room_id}/start")
async def start_game_route(
    room_id: str,
    data: StartRoomRequest,
    db: Session = Depends(get_db),
):
    return start_game(
        db,
        room_id,
        redis_client,
        data.host_id,
    )


@router_room.post("/rooms/{room_code}/ready")
async def ready(
    room_code: str,
    data: PutReady,
):
    return put_ready(room_code, data.player_id)


@router_room.delete("/rooms/{room_code}/delete")
async def delete(
    room_code: str,
    data: DeletePlayer,
):
    return delete_player(
        room_code,
        data.host_id,
        data.target_id,
    )