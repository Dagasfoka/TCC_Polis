# Schemas de criar/entrar/sair de sala.
from pydantic import BaseModel


class RoomCode(BaseModel):
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
class ExitRoomRequest(BaseModel):
    player_id: str
class CreateRoomRequest(BaseModel):
    host_id: str
    is_private: bool = False
class RandomRoomRequest(BaseModel):
    player_id: str
class ChangePrivacyRequest(BaseModel):
    host_id: str
    is_private: bool
class ChoosePartyRequest(BaseModel):
    player_id: str
    party_id: str