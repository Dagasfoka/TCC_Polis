from typing import TypedDict


class RoomPlayer:
    player_id: str
    ready: bool 
    host: bool 
    party_id: str | None = None