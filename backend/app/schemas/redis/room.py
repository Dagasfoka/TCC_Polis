# Schemas de criar/entrar/sair de sala.
from pydantic import BaseModel


class RoomCreate(BaseModel):
    room_code:str
class StartRoomRequest(BaseModel):
    host_id: str
class JoinRoomRequest(BaseModel):
    player_id: str
class PutReady(BaseModel):
    player_id: str
class DeletePlayer(BaseModel):
    host_id : str
    target_id : str