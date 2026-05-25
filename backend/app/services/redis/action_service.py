import random

from backend.app.factories.redis.action_factory import (
    build_action_response_before_question,
)
from backend.app.rules.action_rule import (
    adjust_success_chance_by_answer,
)
from backend.app.services.banco.action_option_service import (
    get_all_options_by_type,
    get_option_by_id,
)
from backend.app.services.banco.question_service import (
    get_next_question_for_player,
)
from backend.app.services.redis.match_mission_service import (
    final_round_verify,
    start_round_verify,
)
from backend.app.services.redis.match_service import (
    build_match_pending_action_question,
    get_match_by_id,
    save_match,
)
from backend.app.validators import (
    verifty_pending_action_question_exist,
    verify_current_player_turn,
    verify_match_exist,
    verify_match_is_running,
    verify_option_exist,
    verify_pending_action_question_player,
    verify_player_exist,
    verify_target_exist,
    verify_target_owner,
)

QUESTION_CORRECT_BONUS = 20
QUESTION_WRONG_PENALTY = 20
#ERRO?
#DIFF : HIGH MULTIVERSE ++


def get_attack_options():
    return get_all_options_by_type("attack")

#ERROR? def mt grande
#antiga resolve_attack_option
def prepare_attack_option(
    match_id,
    player_id: str,
    target_territory_id: str,
    option_id: str,
):
    """
    Essa função:
    Salva no match uma ação pendente, guardando qual jogador, território, opção e pergunta estão ligados a essa 
tentativa de ataque.
    Retorna para o front os dados da ação e da pergunta, para ele saber o que exibir antes de resolver o ataque.
    """
    match: dict = get_match_by_id(match_id)
    
    verify_match_exist(match)
    verify_match_is_running(match)
    verify_current_player_turn(player_id)
    option = get_option_by_id(option_id)
    
    verify_option_exist(option)


    target = find_territory(match, target_territory_id)

    verify_target_exist(target)
    verify_target_owner(target,player_id)

    player = find_player(match, player_id)
    verify_player_exist(player)

    if match.get("round") % 3 == 0 or "ENZO" == "ENZO":
        # ERRO{
        question = get_next_question_for_player(player)
        match["pending_action_question"]=build_match_pending_action_question(player_id,target_territory_id,option_id,question)
        save_match(match)
        action_response=build_action_response_before_question(
            response_type = "attack_response",
            player_id = player_id,
            target= target,
            target_territory_id = target_territory_id,
            option =option,
            question=question
            )
        return {
            "match": match,
            "action_response":action_response
        }
    # } ERRO
    #Diff : MID
    else:
        return resolve_attack_no_question(match_id,player_id,target_territory_id, option)
    

#ERRO{
def resolve_attack_no_question(
    match_id,
    player_id: str,
    target_territory_id,
    option,
):
    match = get_match_by_id(match_id)

    if match is None:
        raise ValueError("Partida não encontrada")

    if match["status"] != "running":
        raise ValueError("Partida não está em andamento")

    if match["current_turn_player_id"] != player_id:
        raise ValueError("Não é o turno desse jogador")

    action_result = execute_attack_roll(
        match=match,
        player_id=player_id,
        target_territory_id=target_territory_id,
        option=option,
        success_chance=option["success_chance"],
    )

    match.pop("pending_action_question", None)

    match["last_action_result"] = action_result

    save_match(match)

    won = final_round_verify(match_id, player_id)

    if won:
        match = get_match_by_id(match_id)
        match["status"] = "finished"
        match["winner_id"] = player_id
        match["last_action_result"] = action_result
        save_match(match)

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

    match = get_match_by_id(match_id)

    advance_turn(match)

    save_match(match)

    start_round_verify(match_id, match["current_turn_player_id"])

    match = get_match_by_id(match_id)
    match["last_action_result"] = action_result

    save_match(match)

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
# }ERRO
# Diff : HIGH
#ERRO {
def resolve_attack_question(
    match_id,
    player_id: str,
    answer: bool,
):
    """
    Essa função é chamada depois que o jogador responde Verdadeiro/Falso.

    Ela:
    1. confere a resposta;
    2. ajusta a chance da action_option;
    3. rola o dado;
    4. aplica o resultado;
    5. verifica vitória;
    6. avança turno.
    """

    match : dict = get_match_by_id(match_id)

    verify_match_exist(match)
    verify_match_is_running(match)
    verify_current_player_turn(match,player_id)
    
    pending_action_question: dict = match.get("pending_action_question")

    verifty_pending_action_question_exist(pending_action_question)
    verify_pending_action_question_player(pending_action_question,player_id)

    target_territory_id = pending_action_question["target_territory_id"]
    option_id = pending_action_question["option_id"]

    option = get_option_by_id(option_id)

    verify_option_exist(option)

    target = find_territory(match, target_territory_id)

    verify_target_exist(target)
    verify_target_owner(target,player_id)

    correct_answer = pending_action_question["correct_answer"]
    question_was_correct = (answer == correct_answer)

    base_success_chance = option["success_chance"]

    adjusted_success_chance,=adjust_success_chance_by_answer(
        base_success_chance=base_success_chance,
        question_was_correct=question_was_correct
        )

    action_result = execute_attack_roll(
        match=match,
        player_id=player_id,
        target_territory_id=target_territory_id,
        option=option,
        base_success_chance=base_success_chance,
        adjusted_success_chance=adjusted_success_chance,
        question_was_correct=question_was_correct,
        correct_answer=correct_answer,
        player_answer=answer,
        question_id=pending_action_question.get("question_id"),
    )
    match.pop("pending_action_question", None)

    match["last_action_result"] = action_result

    save_match(match)

    won = final_round_verify(match_id, player_id)

    if won:
        match["status"] = "finished"
        match["winner_id"] = player_id
        match["last_action_result"] = action_result
        save_match(match)

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

    match = get_match_by_id(match_id)

    advance_turn(match)

    save_match(match)

    start_round_verify(match_id, match["current_turn_player_id"])

    match = get_match_by_id(match_id)
    match["last_action_result"] = action_result

    save_match(match)

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

# }ERRO
# Diff : HIGH
#ERRO {
def execute_attack_roll(
    match: dict,
    player_id: str,
    target_territory_id: str,
    option: dict,
    base_success_chance: int,
    adjusted_success_chance: int,
    question_was_correct: bool,
    correct_answer: bool,
    player_answer: bool,
    question_id,
):
    """
    Essa função mantém a lógica antiga da sua resolve_attack_option.

    A diferença é que agora ela usa adjusted_success_chance
    em vez de option["success_chance"] diretamente.
    """

    target = find_territory(match, target_territory_id)

    verify_target_exist(target)

    roll = random.randint(1, 100)
    minimum_roll_to_succeed = 100 - adjusted_success_chance
    success = roll >= minimum_roll_to_succeed

    influence_generated = 0
    conquered = False
    leftover = 0

    old_owner_id = target["owner_id"]
    old_current_influence = target["current_influence"]

    if success:
        influence_generated = option["influence_generated"]

        current_influence = target["current_influence"]
        base_influence = target["base_influence"]

        if influence_generated > current_influence:
            conquered = True
            leftover = influence_generated - current_influence

            target["owner_id"] = player_id
            target["current_influence"] = base_influence + leftover
        else:
            target["current_influence"] = current_influence - influence_generated

    action_result = {
        "type": "attack_result",

        "success": success,
        "roll": roll,

        "question_id": question_id,
        "question_was_correct": question_was_correct,
        "player_answer": player_answer,
        "correct_answer": correct_answer,

        "base_success_chance": base_success_chance,
        "adjusted_success_chance": adjusted_success_chance,
        "success_chance": adjusted_success_chance,
        "minimum_roll_to_succeed": minimum_roll_to_succeed,

        "option": option,
        "option_id": option["option_id"],
        "title": option["title"],
        "description": option["description"],
        "risk_level": option["risk_level"],
        "cost_money": option["cost_money"],

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
# }ERRO
# Diff : HIGH

#ERRO{
def find_player(match: dict, player_id: str):
    for player in match["players"]:
        if player["player_id"] == player_id:
            return player

    return None
#}ERRO
#DIFF : EASY
#ERRO {
def find_territory(match: dict, territory_id: str):
    for territory in match["territories"]:
        if territory["territory_id"] == territory_id:
            return territory

    return None
#}ERRO
#DIFF : EASY
#ERRO {
def advance_turn(match: dict):
    players = match["players"]
    current_player_id = match["current_turn_player_id"]

    current_index = 0

    for index, player in enumerate(players):
        if player["player_id"] == current_player_id:
            current_index = index
            break

    next_index = (current_index + 1) % len(players)

    if next_index == 0:
        match["round"] += 1

    match["current_turn_player_id"] = players[next_index]["player_id"]
#} ERRO 
# DIFF : LOW-MID