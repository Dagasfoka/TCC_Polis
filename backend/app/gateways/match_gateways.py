
from backend.app.repositories.redis.match_repo import MatchRepo

class MatchGateway:
    #__________________
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
    def get_round(self,match_dict):
        return match_dict['round']
    #_________________
    def find_player(self,match_dict: dict, player_id: str):
        for player in match_dict["players"]:
            if player["player_id"] == player_id:
                return player
        return None
    def find_territory(self,match_dict: dict, territory_id: str):
        for territory in match_dict["territories"]:
            if territory["territory_id"] == territory_id:
                return territory
        return None