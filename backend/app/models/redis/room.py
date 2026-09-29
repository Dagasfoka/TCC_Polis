from dataclasses import dataclass, field


@dataclass
class Room:
    room_code: str
    is_private: bool = False
    players: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "room_code": self.room_code,
            "is_private": self.is_private,
            "players": self.players
        }