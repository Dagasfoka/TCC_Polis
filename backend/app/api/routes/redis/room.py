# Criar sala, entrar em sala, sair da sala.
from urllib import response

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
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
    ChoosePartyRequest,
)

from backend.app.services.redis.room_service import RoomService

router_room = APIRouter()
templates = Jinja2Templates(directory="templates")

room_service=RoomService()
@router_room.get("/rooms/{room_code}")
def get_room_route(room_code: str):
    return room_service.get_room(room_code)

    
@router_room.post("/rooms", response_model=RoomCode)
def post_room(data: CreateRoomRequest):
    return room_service.create_room(
        host_player_id=data.host_id,
        is_private=data.is_private
    )

@router_room.post("/rooms/random")
def random_room(data: RandomRoomRequest):
    return room_service.join_random_room(data.player_id)

@router_room.post("/rooms/{room_code}/join")
async def join_room_route(room_code: str, data: JoinRoomRequest):
    return room_service.join_room(
        player_id=data.player_id,
        room_code=room_code,
    )

@router_room.post("/rooms/{room_id}/start")
async def start_game_route(
    room_id: str,
    data: StartRoomRequest,
    db: Session = Depends(get_db),
):
    return room_service.start_game(
        db,
        room_id,
        data.host_id,
    )


@router_room.post("/rooms/{room_code}/ready")
async def ready(
    room_code: str,
    data: PutReady,
):
    return room_service.put_ready(room_code, data.player_id)



@router_room.delete("/rooms/{room_code}/exit",response_model=RoomCode)
def exit_room_route(
    room_code: str,
    data: ExitRoomRequest
):

    return room_service.exit_room(
        room_code,
        data.player_id
    )
@router_room.delete("/rooms/{room_code}/kick",response_model=RoomCode)
async def delete(
    room_code: str,
    data: DeletePlayer,
):
    return room_service.delete_player(
        room_code,
        data.host_id,
        data.target_id,
    )

@router_room.patch("/rooms/{room_code}/privacy")
async def change_privacy_route(
    room_code: str,
    data: ChangePrivacyRequest
):
    return room_service.change_room_privacy(
        room_code=room_code,
        host_id=data.host_id,
        is_private=data.is_private
    )

@router_room.patch("/rooms/{room_code}/party")
def choose_party_route(
    room_code: str,
    data: ChoosePartyRequest,
    db: Session = Depends(get_db),
):
    return room_service.choose_party(
        db=db,
        room_code=room_code,
        player_id=data.player_id,
        party_id=data.party_id,
    )