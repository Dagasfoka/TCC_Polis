from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from backend.app.api.routes.redis.match import router_match
from backend.app.api.routes.redis.player import router_player
from backend.app.api.routes.redis.room import router_room
from backend.app.api.routes.redis.websocket import router_websocket

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index_backend.html",
    )

router.include_router(router_match)
router.include_router(router_room)
router.include_router(router_player)
router.include_router(router_websocket)
