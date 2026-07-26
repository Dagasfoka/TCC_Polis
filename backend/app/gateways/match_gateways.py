
from backend.app.repositories.redis.match_repo import MatchRepo

class MatchGateway:
    def __init__(self,match_id,redis_client):
        self.match_repository=MatchRepo(match_id,redis_client)
    async def get_all_players(self):
        match_dict=await self.match_repository.get_match()
        if match_dict is None:
            return None
        players= match_dict['players']
        return players