from backend.app.models.redis.match_mission_test import MatchMission

#Pertence de fato à esse arquivo (factories pois "cria" algo mesmo que nao seja do banco)
class MatchMissionFactory:
    def __init__(self,match_id):
        self.match_id=match_id
    def create_match_mission(self,mission,player):
        match_mision=MatchMission(match_id=self.match_id,mission=mission,owner_id=player)
        return match_mision.to_dict()