import random

from backend.app.factories.match_factory import MatchFactory
from backend.app.gateways.match_gateways import MatchGateway
from backend.app.gateways.player_gateways import PlayerGateway
from backend.app.validators.action_validators import ActionValidator
from backend.app.validators.db.territory_validator import TerritoryValidator
from backend.app.validators.match_mission_validators import MatchMissionValidator
from backend.app.gateways.db.territory_gateway import TerritoryGateway
from backend.app.gateways.match_action_gateway import MatchActionGateway
from backend.app.factories.action_factory import ActionsFactory
from backend.app.factories.match_action_factory import MatchActionFactory
from backend.app.validators.match_territory_validator import MatchTerritoryValidator
from backend.app.validators.match_validators import MatchValidator
from backend.app.validators.pending_action_validators import PendingActionValidator
from backend.app.validators.player_validators import PlayerValidator
from backend.app.models.redis.pending_action import PendingAction
QUESTION_CORRECT_BONUS = 2
QUESTION_WRONG_PENALTY = 2

MIN_SUCCESS_CHANCE = 1
MAX_SUCCESS_CHANCE = 19

match_mission_validator=MatchMissionValidator()
match_territory_validator=MatchTerritoryValidator()

match_gateway=MatchGateway()
territory_gateway=TerritoryGateway()
match_factory=MatchFactory()
match_validator=MatchValidator()
action_factory = ActionsFactory()
player_gateway=PlayerGateway()
player_validator=PlayerValidator()

match_action_gateway=MatchActionGateway()
action_validator=ActionValidator()
match_action_factory = MatchActionFactory()

pending_action_validator=PendingActionValidator()

territory_validator=TerritoryValidator()


def get_attack_actions():
    return action_factory.get_actions_by_type("attack")

def get_defense_actions():
    return action_factory.get_actions_by_type("defense")

def get_match_attack_actions(match_id : int):
    return match_action_gateway.get_all_match_actions(match_id,"attack")

def get_match_defense_actions(match_id : int):
    return match_action_gateway.get_all_match_actions(match_id,"defense")

def prepare_attack_action(
    match_id,
    player_id: str,
    target_territory_id: str,
    option_id: int,
    action_type:str
):
    status="running"
    
    match =match_gateway.get_match(match_id)
    match=match_validator.match_exist(match)
    match=match_validator.verify_match_status(match,status)
    match=match_validator.verify_current_turn_player_id(match,player_id)
    round=match_gateway.get_round(match)
    round=match_validator.round_exist(round)

    target = match_gateway.find_territory(match, target_territory_id)
    target=match_territory_validator.territory_exist(target)
    target=match_territory_validator.verify_territory_owner_id(target,player_id,action_type)

    action = match_action_factory.get_action_by_id(match_id,option_id, action_type)
    action = action_validator.action_exist(action)
    
    player = match_gateway.find_player(match, player_id)
    player=player_validator.not_exist(player)

    if action_type == "attack":
        match_territory_validator.frontier_verify(
            target_territory_id=target_territory_id,
            player_id=player_id,
            match_territories=match['territories'],
            )
    if (round%2)==0:
        question,name_list_questions = match_gateway.get_next_question(match_id)
        match_factory.switch_question_list(match,question,name_list_questions)
        newPendingValue= PendingAction.create_dict(
            player_id=player_id,
            target_territory_id=target_territory_id,
            option_id=option_id,
            question_id=question["question_id"],
            correct_answer=question["answer"],
            action_type = action_type
        )
        key="pending_action"
        match=match_factory.change_key_value(match,key,newPendingValue)
        match_factory.update_match(match)
        
        actionType="attack_question"
        return {
            "match": match,
            "result": {
                "type": actionType,
                "question": {
                "question_id": question['question_id'],
                "subject": question['subject'],
                "description": question['description'],
                "exam_board": question['exam_board'],
                "options": question['options'],
                "difficulty": question['difficulty'],
                "explanation": question['explanation'],
                },
            },
        }
    else:
        type="attack_no_question"
        return resolve_action_no_question(match_id,player_id,action,target_territory_id,type,action_type)

def resolve_action_no_question(
    match_id : int,
    player_id: str,
    action : dict,
    target_territory_id: str,
    type : str,
    action_type:str
):

    print("Chegou até aqui")
    match = match_gateway.get_match(match_id)
    match=match_validator.match_exist(match)

    action = action_validator.action_exist(action)

    target = match_gateway.find_territory(match, target_territory_id)
    target = match_territory_validator.territory_exist(target)
    target = match_territory_validator.verify_territory_owner_id(target,player_id,action_type)



    base_success_chance = action["success_chance"]

    action_result = execute_attack_roll(
        match=match,
        player_id=player_id,
        target_territory_id=target_territory_id,
        option=action,
        base_success_chance=base_success_chance,
        type=type,
    )

    match["last_action_result"] = action_result

    match_factory.update_match(match)

    won = match_mission_validator.final_round_verify(match_id, player_id)

    if won:
        match=match_factory.finish_match(match,player_id,action_result)
        match_factory.update_match(match)

        return {
            "match": match,
            "result": {
                **action_result,
                "next_turn_player_id": match["current_turn_player_id"],
                "round": match["round"],
                "winner_id": player_id,
                "status": "finished",
            },
        }

    match_factory.advance_turn(match)

    match_factory.update_match(match)

    match_mission_validator.start_round_verify(match_id, match["current_turn_player_id"])

    match["last_action_result"] = action_result

    match_factory.update_match(match)

    return {
        "match": match,
        "result": {
            **action_result,
            "next_turn_player_id": match["current_turn_player_id"],
            "round": match["round"],
            "winner_id": match.get("winner_id"),
            "status": match["status"],
        },
    }

def resolve_attack_action(
    match_id,
    player_id: str,
    answer: bool,
    action_type:str
):
    status="running"
    match = match_gateway.get_match(match_id)
    match=match_validator.match_exist(match)
    match=match_validator.verify_match_status(match,status)
    match=match_validator.verify_current_turn_player_id(match,player_id)
    
    pending_action = match.get("pending_action")
    
    pending_action_validator.pending_action_exist(pending_action)
    pending_action_validator.verify_pending_action_player_id(pending_action,player_id)


    target_territory_id = pending_action["target_territory_id"]
    option_id = pending_action["option_id"]

    action = match_action_gateway.get_match_action_by_id(match_id,option_id,action_type)
    action = action_validator.action_exist(action)

    target = match_gateway.find_territory(match, target_territory_id)
    target = match_territory_validator.territory_exist(target)
    target = match_territory_validator.verify_territory_owner_id(target,player_id,action_type)


    correct_answer = pending_action["correct_answer"]
    question_was_correct = answer == correct_answer
    base_success_chance = action["success_chance"]

    adjusted_success_chance = clamp_success_chance(question_was_correct,base_success_chance)
    type="attack_result"
    action_result = execute_attack_roll(
        match=match,
        player_id=player_id,
        target_territory_id=target_territory_id,
        option=action,
        base_success_chance=base_success_chance,
        type=type,
        adjusted_success_chance=adjusted_success_chance,
        question_was_correct=question_was_correct,
        correct_answer=correct_answer,
        player_answer=answer,
        question_id=pending_action["question_id"],
    )
    key="pending_action"
    match=match_factory.clean_key_value(key,match)

    match["last_action_result"] = action_result

    match_factory.update_match(match)

    won = match_mission_validator.final_round_verify(match_id, player_id)

    if won:
        match["status"] = "finished"
        match["winner_id"] = player_id
        match["last_action_result"] = action_result
        match_factory.update_match(match)

        return {
            "match": match,
            "result": {
                **action_result,
                "next_turn_player_id": match["current_turn_player_id"],
                "round": match["round"],
                "winner_id": player_id,
                "status": "finished",
            },
        }

    match_factory.advance_turn(match)

    match_factory.update_match(match)

    match_mission_validator.start_round_verify(match_id, match["current_turn_player_id"])

    match["last_action_result"] = action_result

    match_factory.update_match(match)

    return {
        "match": match,
        "result": {
            **action_result,
            "next_turn_player_id": match["current_turn_player_id"],
            "round": match["round"],
            "winner_id": match.get("winner_id"),
            "status": match["status"],
        },
    }


def execute_attack_roll(
    match: dict,
    player_id: str,
    target_territory_id: str,
    option: dict,
    base_success_chance: int,
    type,
    adjusted_success_chance: int | None=None,
    question_was_correct: bool | None=None,
    correct_answer: bool | None=None,
    player_answer: bool | None=None,
    question_id: int | None=None,
):
    """
    Essa função mantém a lógica antiga da sua prepare_attack_action.

    A diferença é que agora ela usa adjusted_success_chance
    em vez de option["success_chance"] diretamente.
    """
    print("Chegou até aqui 2")
    player = match_gateway.find_player(match, player_id)
    player=player_validator.not_exist(player)
    
    target = match_gateway.find_territory(match, target_territory_id)
    target=match_territory_validator.territory_exist(target)

    roll = random.randint(1, 20)
    if adjusted_success_chance is not None:
        minimum_roll_to_succeed = adjusted_success_chance
    else:
        minimum_roll_to_succeed = base_success_chance
    success = roll >= minimum_roll_to_succeed

    influence_generated = 0
    money_generated = -option["cost"]
    
    
    corruption_generated = option["corruption"]
    if success:
        money_generated = option["money"]
        influence_generated = option["influence"]
        response = option["responses"]["normal_success"]
        if roll >= option["positive_critical"]:
            influence_generated += influence_generated/2
            money_generated += option["cost"]
            response = option["responses"]["high_critical"]
    else:
        response = option["responses"]["normal_fail"]
        if roll <= option["negative_critical"]:
            influence_generated = -option["influence"]/2
            money_generated -= option["cost"]
            response = option["responses"]["low_critical"]

    money_generated = money_generated 
    conquered = False
    leftover = 0

    old_owner_id = target["owner_id"]
    old_current_influence = target["current_influence"]
    current_influence = target["current_influence"]
    base_influence = target["base_influence"]

    if success:
        
        if option["action_type"] == "attack":
            if influence_generated >= current_influence:
                conquered = True
                leftover = influence_generated - current_influence

                target["owner_id"] = player_id
                target["current_influence"] = base_influence + leftover
            else:
                target["current_influence"] = current_influence - influence_generated
        else:
            conquered = True
            target["current_influence"] = current_influence + influence_generated
    elif influence_generated < 0:
        negative_influence = influence_generated
        if option["action_type"] == "attack":
            conquered = False
            territory = territory_gateway.get_territory_by_id(target_territory_id)
            territory=territory_validator.territory_exist(territory)
            player_territories = match_gateway.get_your_territories(match,player_id)

            frontier_player_territories = [
                territory_player
                for territory_player in player_territories
                if territory_player["territory_id"] in territory.frontiers
            ]
            random.shuffle(frontier_player_territories)
            for territory_player in frontier_player_territories:
                if territory_player["current_influence"] > -negative_influence:
                    territory_player["current_influence"] += negative_influence
                    break
                else:
                    negative_influence += territory_player["current_influence"] - 1
                    territory_player["current_influence"] = 1
        else:
            conquered = True
            target["current_influence"] = current_influence + influence_generated
            if target["current_influence"] <= 0:
                    target["current_influence"] = 1

    player["match_money"] += money_generated
    player["match_corruption"] += corruption_generated
    player["match_influence"] += influence_generated

    action_result = {
        "type": type,

        "success": success,
        "roll": roll,

        "question_id": question_id,
        "question_was_correct": question_was_correct,
        "player_answer": player_answer,
        "correct_answer": correct_answer,

        "base_success_chance": base_success_chance,
        "adjusted_success_chance": adjusted_success_chance,
        "success_chance": (
            adjusted_success_chance
            if adjusted_success_chance is not None
            else base_success_chance
        ),
        "minimum_roll_to_succeed": minimum_roll_to_succeed,

        "option": option,
        "option_id": option["action_id"],
        "title": option["title"],
        "description": option["description"],
        "risk_level": option["risk_level"],
        "cost_money": option["cost"],
        "money_generated":money_generated,
        "new_money_player":player["match_money"],
        "new_corruption_player":player["match_corruption"],
        "new_influence_player":player["match_influence"],
        "response": response,
        "corruption_generated":corruption_generated,

        "target_territory_id": target_territory_id,
        "territory_id": target_territory_id,
        "territory_name": target["name"],

        "old_owner_id": old_owner_id,
        "new_owner_id": target["owner_id"],
        "previous_owner_id": old_owner_id,

        "old_current_influence": old_current_influence,
        "new_current_influence": target["current_influence"],
        "previous_influence": old_current_influence,
        "new_influence": target["current_influence"],

        "influence_generated": influence_generated,
        "conquered": conquered,
        "leftover": leftover,
    }

    return action_result

def clamp_success_chance(question_was_correct,base_success_chance):
    if question_was_correct:
        adjusted_success_chance = base_success_chance - QUESTION_CORRECT_BONUS
    else:
        adjusted_success_chance = base_success_chance + QUESTION_WRONG_PENALTY
    return max(MIN_SUCCESS_CHANCE, min(MAX_SUCCESS_CHANCE, adjusted_success_chance))