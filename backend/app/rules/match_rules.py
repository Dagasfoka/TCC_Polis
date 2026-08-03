from backend.app.gateways.match_gateways import MatchGateway
from backend.app.gateways.missions_gateways import MissionsGateway
from backend.app.gateways.questions_gateways import QuestionGateways

from backend.app.rules.missions_rules import MissionsRules

from backend.app.factories.match_mission_factory_test import MatchMissionFactory

import random

def distribute_initial_territories_missions_questions(db, redis_client,match_state_dict):
    #Gateways
    missions_gateway=MissionsGateway(db=db)
    questions_gateway = QuestionGateways()
#____________________
    players = match_state_dict["players"]
    missions = missions_gateway.get_all_missions()
    questions=questions_gateway.get_all_questions()
#____________________
    #Rules (dentro provalmente tem que repartir Gateways e factories)
    match_state_dict["missions"] =(
        distribute_match_missions(
        db=db,
        match_id=match_state_dict["match_id"],
        players=players,
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

def distribute_questions(match_state_dict):
    questions_gateway = QuestionGateways()
    questions=questions_gateway.get_all_questions()

    
    for player in match_state_dict["players"]:
        player_questions = [question.copy() for question in questions]
        random.shuffle(player_questions)
        player["questions"] = player_questions
    return match_state_dict

def distribute_match_missions(match_id, players,db):
    missions_gateway=MissionsGateway(db=db)
    missions=missions_gateway.get_all_missions()

    match_missions_factory=MatchMissionFactory(match_id=match_id)

    missions_rules=MissionsRules(missions=missions)
    chosen_missions=missions_rules.choose_missions(quantity_players=len(players))

    #validator
    if len(players) != len(chosen_missions):
        raise ValueError("A quantidade de players precisa ser igual à quantidade de missões.")

    match_missions = []

    for player, mission in zip(players, chosen_missions):
        content = mission.content.copy()

        if mission.type == "destruction":
            content["destruction"] = choose_destruction_target(
                players=players,
                owner_id=player["player_id"],
            )
            mission.content=content
        match_mission= match_missions_factory.create_match_mission(mission=mission,player=player)

        match_missions.append(match_mission)
        print(match_missions)
    return match_missions

def choose_destruction_target(players, owner_id):
    possible_targets = [
        player["player_id"]
        for player in players
        if player["player_id"] != owner_id
    ]

    if not possible_targets:
        raise ValueError("Não há alvo possível para missão de destruição.")

    return random.choice(possible_targets)