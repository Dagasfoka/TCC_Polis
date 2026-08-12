from typing import TypedDict

class RoomPlayer(TypedDict):
    player: dict
    ready: bool
    host: bool
from dataclasses import dataclass, field

@dataclass
class Room:
    lobby_id: str
    players: dict[str, RoomPlayer] = field(default_factory=dict)
    def to_dict(self):
        return {
            "lobby_id": self.lobby_id,
            "players": [
                room_player["player"]["player_id"]
                for room_player in self.players.values()
            ]
        }