from pydantic import BaseModel


class PlayerCreate(BaseModel):
    username: str


class UserPlayerCreate(BaseModel):
    user_id: int


class PlayerDelete(BaseModel):
    player_id: str


class UserPlayerDelete(BaseModel):
    user_id: int


class PlayerRoom(BaseModel):
    host_id: str