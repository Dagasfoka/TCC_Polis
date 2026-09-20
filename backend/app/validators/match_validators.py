from backend.app.models.db import territory
from backend.app.repositories.redis.match_repo import (
    get_match_state,
    get_territory_by_id,
    get_territory_by_region,
)
class MatchValidator:
    def __init__(self) -> None:
        pass
#_________________________________________________ Simples
    def match_exist(self,match_dict):
        if match_dict is None:
           raise Exception("Partida não existe") 
        return match_dict 
    def territory_exist(self,territory):
        if territory is None:
           raise Exception("Território não existe") 
        return territory 
#_________________________________________________ AUX
    def is_alive(self,match_id, target_id):
        match_dict = get_match_state(match_id)
        match_dict=self.match_exist(match_dict)
        territories = match_dict["territories"]

        for territory in territories:
            if territory["owner_id"] == target_id:
                return True

        return False


    def verify_state(self,states_id: list[str], owner_id: str, match_id: str):
        match_dict = get_match_state(match_id)

        for state_id in states_id:
            state=get_territory_by_id(match_dict, state_id)
            state=self.territory_exist(state)
            if state["owner_id"] != owner_id:
                return False

        return True


    def verify_region(self,region: str, quantity: int, match_id, owner_id: str) -> bool:
        match_dict = get_match_state(match_id)

        territories = get_territory_by_region(match_dict, region)

        owned_territories = [
            territory for territory in territories
            if territory["owner_id"] == owner_id
        ]

        return len(owned_territories) >= quantity