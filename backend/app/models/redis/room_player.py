from typing import TypedDict


class RoomPlayer(TypedDict):
    player_id: str
    ready: bool
    host: bool
