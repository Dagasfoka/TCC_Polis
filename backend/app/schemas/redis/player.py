# Schemas públicos do jogador.
from pydantic import BaseModel


class PlayerCreate(BaseModel):
    username:str
class PlayerRoom(BaseModel):
    host_id:str