from dataclasses import dataclass


@dataclass
class MatchMission:
    match_id: int
    mission_id: int
    type: str
    content: dict
    owner_id: str

    def to_dict(self):
        return {
            "match_id": self.match_id,
            "mission_id": self.mission_id,
            "type": self.type,
            "content": self.content,
            "owner_id": self.owner_id,
        }