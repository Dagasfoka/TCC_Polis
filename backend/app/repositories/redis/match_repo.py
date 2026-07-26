# Busca/salva estado da partida no Redis.
from json import dumps, loads
from redis import Redis
from backend.app.db.redis import redis_client


class MatchRepo:
    def __init__(self, match_id,redis_client):
        self.match_id = match_id
        self.redis_client : Redis =redis_client
        
    async def get_match(self):
            key = f"match:{self.match_id}:state"
    
            match_state = await self.redis_client.get(key)
    
            if match_state is not None:
                return loads(match_state)
    
            return None
    
    async def save_match_state(self, match_dict : dict) -> None:
        match_state_JSON = dumps(match_dict)
        key = f"match:{match_dict['match_id']}:state"

        await self.redis_client.set(key, match_state_JSON)
    
    async def incr_match_round(self):
        return await self.redis_client.incr(
            f"match:{self.match_id}:round"
        )

    async def generate_match_id(self) -> int:
        return await self.redis_client.incr("match:counter")

def incr_match_round(match_id):
    return redis_client.incr(f"match:{match_id}:round")

def generate_match_id() -> int:
    return redis_client.incr("match:counter")
        
def save_match_state(match_state_dict):
    match_state_JSON=  dumps(match_state_dict)
    key = f"match:{match_state_dict['match_id']}:state"
    redis_client.set(key,match_state_JSON)


def get_match_state(match_id):
    key = f"match:{match_id}:state"
    match_state=redis_client.get(key)
    if match_state is not None:
        return loads(match_state)
    return None
#Rules{
def get_territory_by_region(match_dict,region):
    territories=match_dict['territories']
    territories_region=[]
    for t in territories:
        if t["region"] == region:
            territories_region.append(t)
    return territories_region
            

def get_territory_by_id(match_dict,territory_id):
    for territory in match_dict['territories']:
        if territory['territory_id'] == territory_id:
            return territory
#}
