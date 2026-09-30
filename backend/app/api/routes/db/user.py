# Rotas HTTP auxiliares da partida.
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from backend.app.schemas.db.user import UserCreate
from backend.app.services.db.user_service import create_user,get_user_by_id, get_all_users

router_user = APIRouter()
templates = Jinja2Templates(directory='templates')

@router_user.post("/users")
async def post_user(data : UserCreate):
    return create_user(username=data.username, password=data.password)

@router_user.get("/users/{user_id}")
async def get_user_route(user_id:str):
    return get_user_by_id(user_id)

@router_user.get("/users")
async def get_all_users_route():
    return get_all_users()
