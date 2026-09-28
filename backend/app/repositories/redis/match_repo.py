# Busca/salva estado da partida no Redis.
from json import dumps, loads
from redis import Redis
from backend.app.db.redis import redis_client


class MatchRepo:
    def __init__(self):
        self.redis_client : Redis =redis_client
        
    def get_match(self,match_id):
            key = f"match:{match_id}:state"
    
            match_state = self.redis_client.get(key)
    
            if match_state is not None:
                return loads(match_state)
    
            return None
    
    def update_match(self, match_dict : dict) -> None:
        match_state_JSON = dumps(match_dict)
        key = f"match:{match_dict['match_id']}:state"

        self.redis_client.set(key, match_state_JSON)
    
    def incr_match_round(self,match_id):
        return self.redis_client.incr(
            f"match:{match_id}:round"
        )

    def generate_match_id(self) -> int:
        return self.redis_client.incr("match:counter")
    
    def get_territory_by_id(self,match_dict,territory_id):
        for territory in match_dict['territories']:
            if territory['territory_id'] == territory_id:
                return territory

    def get_territory_by_region(self,match_dict,region):
        territories=match_dict['territories']
        territories_region=[]
        for t in territories:
            if t["region"] == region:
                territories_region.append(t)
        return territories_region
            


