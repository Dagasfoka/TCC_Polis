# Rotas HTTP auxiliares da partida.
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from backend.app.services.redis.match_service import get_match
from backend.app.scripts.create_demo_match import create_demo_match

router_match = APIRouter()
templates = Jinja2Templates(directory='templates')

@router_match.get("/matches/{match_id}")
async def get_match_route(match_id: str):
    return get_match(match_id)

@router_match.post("/match/create")
async def create_demo_match_route():
    match = create_demo_match()

    return {
        "match_id": match["match_id"]
    }
