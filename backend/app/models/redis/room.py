from dataclasses import dataclass, field

@dataclass
class Room:
    room_code: str
    players: dict = field(default_factory=dict)
    def to_dict(self):
        return {
            "room_code": self.room_code,
            "players": self.players
        }