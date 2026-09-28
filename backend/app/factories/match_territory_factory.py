import random
from backend.app.models.redis.match_territory import MatchTerritory
from backend.app.models.db.territory import Territory
class MatchTerritoryFactory:
    def __init__(self) -> None:
        pass
    
    def distribute_territories(self,players,territories):
        random.shuffle(territories)
        for index, territory in enumerate(territories):
            player = players[index % len(players)]
            territory["owner_id"] = player["player_id"]

        return players
    def build_match_territory(self,match_id,territory_data : Territory):
        match_id = match_id
        territory_id = territory_data.id
        base_influence = territory_data.base_influence
        name = territory_data.name
        region = territory_data.region
        match_territory = MatchTerritory.create_dict(
            match_id, territory_id, base_influence, name, region
        )       
        return match_territory