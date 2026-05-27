import random

from backend.app.factories.redis.match_mission_factory import (
    choose_missions,
    distribute_match_missions,
)
from backend.app.models.redis.match_model import Match
from backend.app.models.redis.match_territory_model import MatchTerritory
from backend.app.repositories.database.mission_repo import get_all_missions
from backend.app.repositories.database.question_repo import list_questions
from backend.app.repositories.database.territory_repo import get_all_territories
from backend.app.repositories.redis.match_repo import generate_match_id

###ERRO Importações conceituais erradas, teria de importar outros services
def build_initial_match_state(db, room_dict) -> Match:
    territories = get_all_territories(db)
    match_territories = []
    match_id = generate_match_id()

    for territory_data in territories:
        match_territory = MatchTerritory(
            match_id=match_id,
            territory_id=territory_data.id,
            base_influence=territory_data.base_influence,
            name=territory_data.name,
            region=territory_data.region,
        )
        match_territories.append(match_territory)
    match_state = Match( #Create no repo
        match_id=match_id,
        territories=match_territories,
        room_code=room_dict["room_code"],
        players=room_dict["players"],
        status="running",
        current_turn_player_id=room_dict["players"][0]["player_id"],
        round=1,
        missions=[],
    )

    return match_state

def build_match_pending_action_question_factory(match:dict,player_id:str,target_territory_id:str,option_id:int,question:dict):
    match["pending_action_question"] = {
            "player_id": player_id,
            "target_territory_id": target_territory_id,
            "option_id": option_id,
            "question_id": question.get("question_id"),
            "correct_answer": question.get("answer"),
        }
    return match

def distribute_initial_territories_missions_questions(db,match_state_dict):
    players = match_state_dict["players"]

    questions = list_questions()
    missions = get_all_missions(db)
    chosen_missions = choose_missions(missions, len(players))

    match_state_dict["missions"] = distribute_match_missions(
        match_id=match_state_dict["match_id"],
        players=players,
        chosen_missions=chosen_missions,
    )

    for player in match_state_dict["players"]:
        player_questions = [question.copy() for question in questions]
        random.shuffle(player_questions)
        player["questions"] = player_questions

    for index, territory in enumerate(sorted(match_state_dict["territories"])):
        player = players[index % len(players)]
        territory["owner_id"] = player["player_id"]

    return match_state_dict