from dataclasses import dataclass
from backend.app.models.db.mission import Mission

@dataclass
class MatchMission:
    #Tirei passar diretamente mission_id,type e content e fiz passar so passando mission. Testar se isso esta dando certo
    match_id: int
    mission: Mission
    owner_id: str

    def to_dict(self):
        return {
            "match_id": self.match_id,
            "mission_id": self.mission.mission_id,
            "type": self.mission.type,
            "content": self.mission.content,
            "owner_id": self.owner_id,
        }