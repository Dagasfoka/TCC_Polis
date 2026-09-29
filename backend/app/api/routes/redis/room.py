# Criar sala, entrar em sala, sair da sala.
from urllib import response

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.schemas.redis.player import PlayerRoom
from backend.app.schemas.redis.room import (
    RoomCode,
    CreateRoomRequest,
    RandomRoomRequest,
    ChangePrivacyRequest,
    StartRoomRequest,
    JoinRoomRequest,
    PutReady,
    DeletePlayer,
    ExitRoomRequest,
)

from backend.app.services.redis.room_service import (
    create_room,
    join_room,
    join_random_room,
    change_room_privacy,
    start_game,
    put_ready,
    delete_player,
    get_room,
    exit_room,
)

router_room = APIRouter()
templates = Jinja2Templates(directory="templates")


@router_room.get("/rooms/{room_code}")
def get_room_route(room_code: str):
    return get_room(room_code)

    
@router_room.post("/rooms", response_model=RoomCode)
def post_room(data: CreateRoomRequest):
    return create_room(
        host_player_id=data.host_id,
        is_private=data.is_private
    )

@router_room.post("/rooms/random")
def random_room(data: RandomRoomRequest):
    return join_random_room(data.player_id)

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
        data.host_id,
    )


@router_room.post("/rooms/{room_code}/ready")
async def ready(
    room_code: str,
    data: PutReady,
):
    return put_ready(room_code, data.player_id)



@router_room.delete("/rooms/{room_code}/exit",response_model=RoomCode)
def exit_room_route(
    room_code: str,
    data: ExitRoomRequest
):

    return exit_room(
        room_code,
        data.player_id
    )
@router_room.delete("/rooms/{room_code}/kick",response_model=RoomCode)
async def delete(
    room_code: str,
    data: DeletePlayer,
):
    return delete_player(
        room_code,
        data.host_id,
        data.target_id,
    )

@router_room.patch("/rooms/{room_code}/privacy")
async def change_privacy_route(
    room_code: str,
    data: ChangePrivacyRequest
):
    return change_room_privacy(
        room_code=room_code,
        host_id=data.host_id,
        is_private=data.is_private
    )