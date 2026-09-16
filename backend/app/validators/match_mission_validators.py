from backend.app.repositories.redis.match_mission_repo import MatchMissionRepo


class MatchMissionValidator:
    def __init__(self) -> None:
        self.match_mission_repo=MatchMissionRepo()
    def start_verify_match_mission(self,match_id, player_id):
        match_mission = self.match_mission_repo.get_match_mission_by_owner_id(match_id=match_id, owner_id=player_id)

        if match_mission is None:
            raise ValueError("Missão do jogador não encontrada.")

        if match_mission["type"] == "destruction":
            target_id = match_mission["content"]["destruction"]

            if not is_alive(match_id, target_id):
                match_mission["type"] = "state"
                self.match_mission_repo.update_match_mission(match_id, match_mission)
                return True

        return False

    def final_verify_match_mission(self,match_id, player_id):
        match_mission = self.match_mission_repo.get_match_mission_by_owner_id(match_id, player_id)
 
        if match_mission is None:
            raise ValueError("Missão do jogador não encontrada.")
 
        match match_mission["type"]:
            case "region":
                for region_content in match_mission["content"]["region"]:
                    if not verify_region(
                        region_content["region"],
                        region_content["quantity"],
                        match_id,
                        match_mission["owner_id"],
                    ):
                        return False
 
                return True   