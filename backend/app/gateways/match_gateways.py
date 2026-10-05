
import random
from backend.app.repositories.redis.match_repo import MatchRepo
from backend.app.validators.match_validators import MatchValidator

match_validator=MatchValidator()
class MatchGateway:
    #__________________
    def __init__(self):
        self.match_repository=MatchRepo()
    def get_all_players(self,match_id):
        match_dict= self.match_repository.get_match(match_id)
        match_dict=match_validator.match_exist(match_dict)
        players= match_dict['players']
        return players
    def get_match(self,match_id):
        return self.match_repository.get_match(match_id)
    def get_territory_by_id(self,match_dict,territory_id):
        return self.match_repository.get_territory_by_id(match_dict,territory_id)
    def get_territory_by_region(self,match_dict,region):
        return self.match_repository.get_territory_by_region(match_dict,region)
    def get_round(self,match_dict):
        return match_dict['round']
    def get_questions(self, match_id):
        match_dict = match_validator.match_exist(self.get_match(match_id))
        name_list_questions = match_dict["activate_questions_list"]
        questions = match_dict[name_list_questions]

        if not questions:
            name_list_questions = (
                "questions_2"
                if name_list_questions == "questions_1"
                else "questions_1"
            )
            questions = match_dict[name_list_questions]
            match_validator.questions_exist(questions)
            match_dict["activate_questions_list"] = name_list_questions
        return questions, name_list_questions
    #_________________
    def get_next_question(self,match_id):
        questions,name_list_questions=(self.get_questions(match_id))
        question=random.choice(questions)
        return question,name_list_questions
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
    def find_your_mission(self,match: dict, player_id: str):
        missions = match.get("missions", [])

        for mission in missions:
            if mission.get("owner_id") == player_id:
                return mission.get("mission") or mission

        return None

    def get_your_territories(self,match: dict, player_id: str):
        territories = match.get("territories", [])
        player_territories = []
        for territory in territories:
            if territory["owner_id"] == player_id:
                player_territories.append(territory["territory_id"])

        return player_territories