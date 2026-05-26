# Rotas HTTP auxiliares da partida.
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from backend.app.services.match_service import get_match

router_match = APIRouter()
templates = Jinja2Templates(directory='templates')

@router_match.get("/matches/{match_id}")
async def get_match_route(match_id: str):
    return get_match(match_id)