from typing import TypedDict

class RoomPlayer(TypedDict):
    player: dict
    ready: bool
    host: bool