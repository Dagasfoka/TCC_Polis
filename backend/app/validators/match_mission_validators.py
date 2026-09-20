from backend.app.repositories.redis.match_mission_repo import MatchMissionRepo
from backend.app.validators.match_validators import MatchValidator


class MatchMissionValidator:
    def __init__(self) -> None:
        self.match_mission_repo=MatchMissionRepo()
        self.match_validator=MatchValidator()
    def start_round_verify(self,match_id, player_id):
        match_mission = self.match_mission_repo.get_match_mission_by_owner_id(match_id=match_id, owner_id=player_id)

        match_mission=self.match_mission_exist(match_mission)

        if match_mission["type"] == "destruction":
            target_id = match_mission["content"]["destruction"]

            if not self.match_validator.is_alive(match_id, target_id):
                match_mission["type"] = "state"
                self.match_mission_repo.update_match_mission(match_id, match_mission)
                return True

        return False

    def final_round_verify(self,match_id, player_id):
        match_mission = self.match_mission_repo.get_match_mission_by_owner_id(match_id, player_id)
 
        match_mission=self.match_mission_exist(match_mission)
 
        match match_mission["type"]:
            case "region":
                for region_content in match_mission["content"]["region"]:
                    if not self.match_validator.verify_region(
                        region_content["region"],
                        region_content["quantity"],
                        match_id,
                        match_mission["owner_id"],
                    ):
                        return False
 
                return True  
            case "state":
                    return self.match_validator.verify_state(
                        match_mission["content"]["state"],
                        match_mission["owner_id"],
                        match_id,
                    )

            case "destruction":
                return not self.match_validator.is_alive(
                    match_id,
                    match_mission["content"]["destruction"],
                    )

            case _:
                raise ValueError(f"Tipo de missão inválido: {match_mission['type']}")

#_______________________Simples
    def match_mission_exist(self,match_mission):
        if match_mission is None:
           raise Exception("missão não existe") 
        return match_mission