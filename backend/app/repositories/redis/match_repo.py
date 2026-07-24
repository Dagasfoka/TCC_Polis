# Busca/salva estado da partida no Redis.
from json import dumps, loads

from backend.app.db.redis import redis_client


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

