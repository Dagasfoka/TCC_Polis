# Rotas HTTP auxiliares da partida.
from backend.app.core.config import settings
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from backend.app.services.redis.match_service import get_match
from backend.app.scripts.create_demo_match import create_demo_match
from backend.app.scripts.create_db import create_database
from backend.app.scripts.seed_parties import seed_parties
from backend.app.scripts.seed_missions import seed_missions
from backend.app.scripts.seed_territories import seed_territories
from backend.app.scripts.seed_questions import seed_questions

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

@router_match.post("/db/init")
async def init_database():

    create_database()
    seed_parties()
    seed_missions()
    seed_territories()
    seed_questions()

    return {
        "message": "Banco inicializado com sucesso"
    }
