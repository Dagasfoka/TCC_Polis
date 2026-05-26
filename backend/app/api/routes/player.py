# Rotas HTTP auxiliares da partida.
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from backend.app.schemas.player import PlayerCreate
from backend.app.services.player_service import create_player, get_player

router_player = APIRouter()
templates = Jinja2Templates(directory='templates')

@router_player.post("/players")
async def post_player(data : PlayerCreate):
    return create_player(username=data.username)


@router_player.get("/players/{player_id}")
async def get_player_route(player_id:str):
    return get_player(player_id)
