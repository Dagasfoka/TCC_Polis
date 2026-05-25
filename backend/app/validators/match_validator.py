
def verify_match_exist(match_dict):
    if match_dict is None:
        raise ValueError("Partida não encontrada")
def verify_match_is_running(match_dict: dict):
    if match_dict.get("status") != "running":
        raise ValueError("Partida não está em andamento")
def verify_current_player_turn(match: dict, player_id: str):
    if match["current_turn_player_id"] != player_id:
        raise ValueError("Não é o turno desse jogador")
def verifty_pending_action_question_exist(pending_action_question):
    if pending_action_question is None:
        raise ValueError("Não existe pergunta pendente para essa ação")
def verify_pending_action_question_player(pending_action_question,player_id):
    if pending_action_question["player_id"] != player_id:
        raise ValueError("Essa pergunta não pertence a esse jogador")