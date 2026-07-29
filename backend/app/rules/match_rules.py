from backend.app.gateways.match_gateways import MatchGateway
from backend.app.gateways.missions_gateways import MissionsGateway
from backend.app.gateways.questions_gateways import QuestionGateways

from backend.app.rules.missions_rules import MissionsRules

from backend.app.factories.match_mission_factory import (
    distribute_match_missions,
)
from backend.app.factories.missions_factory import distribute_missions

import random
def distribute_questions(match_state_dict):
    questions_gateway = QuestionGateways()
    questions=questions_gateway.get_all_questions()

    
    for player in match_state_dict["players"]:
        player_questions = [question.copy() for question in questions]
        random.shuffle(player_questions)
        player["questions"] = player_questions
    match_state_dict=distribute_missions(match_state_dict=match_state_dict,questions=questions)
    return match_state_dict

def distribute_initial_territories_missions_questions(db, redis_client,match_state_dict):
    #Gateways
    missions_gateway=MissionsGateway(db=db)
    questions_gateway = QuestionGateways()
#____________________
    players = match_state_dict["players"]
    missions = missions_gateway.get_all_missions()
    questions=questions_gateway.get_all_questions()
#____________________
    #Rules
    missions_rules=MissionsRules(missions=missions)
    chosen_missions = missions_rules.choose_missions(quantity_players=len(players))
    #Rules (dentro provalmente tem que repartir Gateways e factories)
    match_state_dict["missions"] =(
        distribute_match_missions(
        match_id=match_state_dict["match_id"],
        players=players,
        chosen_missions=chosen_missions,
        )
    )
    #Rules (fazer função para:)
    for player in match_state_dict["players"]:
        player_questions = [question.copy() for question in questions]
        random.shuffle(player_questions)
        player["questions"] = player_questions
    #Rules (fazer função para:)
    for index, territory in enumerate(match_state_dict["territories"]):
        player = players[index % len(players)]
        territory["owner_id"] = player["player_id"]

    return match_state_dict