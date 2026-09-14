
from backend.app.repositories.redis.match_repo import MatchRepo

class MatchGateway:
    def __init__(self):
        self.match_repository=MatchRepo()
    async def get_all_players(self,match_id):
        match_dict=await self.match_repository.get_match(match_id)
        if match_dict is None:
            return None
        players= match_dict['players']
        return players
    def get_match_by_id(self,match_id):
        return self.match_repository.get_match(match_id)