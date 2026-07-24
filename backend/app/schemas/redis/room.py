# Schemas de criar/entrar/sair de sala.
from pydantic import BaseModel


class RoomCreate(BaseModel):
    room_code:str
class StartRoomRequest(BaseModel):
    player_id: str