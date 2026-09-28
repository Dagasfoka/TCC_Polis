
from backend.app.repositories.redis.match_repo import MatchRepo

class MatchGateway:
    def __init__(self):
        self.match_repository=MatchRepo()
    def get_all_players(self,match_id):
        match_dict= self.match_repository.get_match(match_id)
        if match_dict is None:
            return None
        players= match_dict['players']
        return players
    def get_match_by_id(self,match_id):
        return self.match_repository.get_match(match_id)
    def get_match(self,match_id):
        return self.match_repository.get_match(match_id)
    def get_territory_by_id(self,match_dict,territory_id):
        return self.match_repository.get_territory_by_id(match_dict,territory_id)
    def get_territory_by_region(self,match_dict,region):
        return self.match_repository.get_territory_by_region(match_dict,region)