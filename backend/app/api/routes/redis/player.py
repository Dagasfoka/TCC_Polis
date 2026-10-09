from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from backend.app.schemas.redis.player import (
    PlayerCreate,
    UserPlayerCreate,
    UserPlayerDelete,
    PlayerDelete,
)

from backend.app.services.redis.player_service import (
    create_player,
    get_player,
    create_user_player,
    delete_user_player,
    delete_player,
)


router_player = APIRouter()
templates = Jinja2Templates(directory='templates')



@router_player.get("/players/{player_id}")
async def get_player_route(
    player_id: str
):
    return get_player(
        player_id
    )


@router_player.post("/players")
def create_player_route(
    data: PlayerCreate
):
    return create_player(
        username=data.username
    )


@router_player.post("/players/user")
def create_user_player_route(
    data: UserPlayerCreate
):
    return create_user_player(
        data.user_id
    )


@router_player.delete("/players/user")
def delete_user_player_route(
    data: UserPlayerDelete
):
    return delete_user_player(
        data.user_id
    )


@router_player.delete("/players")
def delete_player_route(
    data: PlayerDelete
):
    return delete_player(
        data.player_id
    ) 