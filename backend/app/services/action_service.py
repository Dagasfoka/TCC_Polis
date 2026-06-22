import random

from backend.app.repositories.action_option_repo import (
    get_option_by_id,
    list_options_by_action,
)
from backend.app.repositories.match_repo import (
    get_match_state,
    save_match_state,
)
from backend.app.services.match_mission_service import (
    final_round_verify,
    start_round_verify,
)


QUESTION_CORRECT_BONUS = 20
QUESTION_WRONG_PENALTY = 20

MIN_SUCCESS_CHANCE = 5
MAX_SUCCESS_CHANCE = 95


def get_attack_options():
    return list_options_by_action("attack")


def resolve_attack_option(
    match_id,
    player_id: str,
    target_territory_id: str,
    option_id: str,
):
    """
    Essa função agora NÃO executa o ataque diretamente.

    Ela só:
    1. valida se a ação pode acontecer;
    2. pega uma pergunta do jogador;
    3. salva uma ação pendente no match;
    4. devolve a pergunta para o front exibir.
    """

    match = get_match_state(match_id)

    if match is None:
        raise ValueError("Partida não encontrada")

    if match["status"] != "running":
        raise ValueError("Partida não está em andamento")

    if match["current_turn_player_id"] != player_id:
        raise ValueError("Não é o turno desse jogador")

    option = get_option_by_id(option_id)

    if option is None:
        raise ValueError("Opção inválida")

    target = find_territory(match, target_territory_id)

    if target is None:
        raise ValueError("Território não encontrado")

    if target["owner_id"] == player_id:
        raise ValueError("Você já controla esse território")

    player = find_player(match, player_id)

    if player is None:
        raise ValueError("Jogador não encontrado")

    question = get_next_question_for_player(player)

    match["pending_attack_question"] = {
        "player_id": player_id,
        "target_territory_id": target_territory_id,
        "option_id": option_id,
        "question_id": question["question_id"],
        "correct_answer": question["answer"],
    }

    save_match_state(match)

    return {
        "match": match,
        "result": {
            "type": "attack_question",
            "player_id": player_id,
            "target_territory_id": target_territory_id,
            "territory_id": target_territory_id,
            "territory_name": target["name"],
            "option_id": option["option_id"],
            "title": option["title"],
            "description": option["description"],
            "risk_level": option["risk_level"],
            "cost_money": option["cost_money"],
            "success_chance": option["success_chance"],
            "question": {
                "question_id": question["question_id"],
                "subject": question["subject"],
                "description": question["description"],
            },
        },
    }


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

    match = get_match_state(match_id)

    if match is None:
        raise ValueError("Partida não encontrada")

    if match["status"] != "running":
        raise ValueError("Partida não está em andamento")

    pending_question = match.get("pending_attack_question")

    if pending_question is None:
        raise ValueError("Não existe pergunta pendente para essa ação")

    if pending_question["player_id"] != player_id:
        raise ValueError("Essa pergunta não pertence a esse jogador")

    if match["current_turn_player_id"] != player_id:
        raise ValueError("Não é o turno desse jogador")

    target_territory_id = pending_question["target_territory_id"]
    option_id = pending_question["option_id"]

    option = get_option_by_id(option_id)

    if option is None:
        raise ValueError("Opção inválida")

    target = find_territory(match, target_territory_id)

    if target is None:
        raise ValueError("Território não encontrado")

    if target["owner_id"] == player_id:
        raise ValueError("Você já controla esse território")

    correct_answer = pending_question["correct_answer"]
    question_was_correct = answer == correct_answer

    base_success_chance = option["success_chance"]

    if question_was_correct:
        adjusted_success_chance = base_success_chance + QUESTION_CORRECT_BONUS
    else:
        adjusted_success_chance = base_success_chance - QUESTION_WRONG_PENALTY

    adjusted_success_chance = clamp_success_chance(adjusted_success_chance)

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
        question_id=pending_question["question_id"],
    )

    match.pop("pending_attack_question", None)

    match["last_action_result"] = action_result

    save_match_state(match)

    won = final_round_verify(match_id, player_id)

    if won:
        match = get_match_state(match_id)
        match["status"] = "finished"
        match["winner_id"] = player_id
        match["last_action_result"] = action_result
        save_match_state(match)

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

    match = get_match_state(match_id)

    advance_turn(match)

    save_match_state(match)

    start_round_verify(match_id, match["current_turn_player_id"])

    match = get_match_state(match_id)
    match["last_action_result"] = action_result

    save_match_state(match)

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

    if target is None:
        raise ValueError("Território não encontrado")

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


def get_next_question_for_player(player: dict):
    questions = player.get("questions", [])
    print(player)
    if not questions:
        raise ValueError("Esse jogador não possui mais perguntas disponíveis")

    question = questions.pop(0)

    return question


def find_player(match: dict, player_id: str):
    for player in match["players"]:
        if player["player_id"] == player_id:
            return player

    return None


def find_territory(match: dict, territory_id: str):
    for territory in match["territories"]:
        if territory["territory_id"] == territory_id:
            return territory

    return None


def clamp_success_chance(success_chance: int):
    return max(MIN_SUCCESS_CHANCE, min(MAX_SUCCESS_CHANCE, success_chance))


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