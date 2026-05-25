# Ataque, defesa, turno, vitória, mapa.
from backend.app.factories.redis.match_factory import (
    build_initial_match_state,
    build_match_pending_action_question_factory,
    distribute_initial_territories_missions_questions,
)
#ERRO{
from backend.app.repositories.redis.match_repo import (
    get_match_mission_by_owner_repo,
    get_match_state,
    save_match_repo,
)
from backend.app.repositories.redis.room_repo import get_room_repo
#ERRO}
# DIFF: MID
def create_match(db,room_code):
    room_dict=get_room_repo(room_code)
    #ERRO{
    if room_dict is None:
        raise ValueError("Sala não encontrada")

    if not room_dict["players"]:
        raise ValueError("Sala sem jogadores")
    #ERRO}
    # DIFF: EASY

    
    match_state=build_initial_match_state(db,room_dict)
    match_state_dict = match_state.to_dict()
    match_state_dict=distribute_initial_territories_missions_questions(db, match_state_dict)
    save_match(match_state_dict)
    return match_state_dict

def get_match_by_id(match_id):
    return get_match_state(match_id)

#ERRO{
def save_match(match_dict):
    return save_match_repo(match_dict)
#ERRO}
# DIFF: EASY

def build_match_pending_action_question(match:dict,player_id:str,target_territory_id:str,option_id:int,question:dict):
    return build_match_pending_action_question_factory(match,player_id,target_territory_id,option_id,question)

#ERRO{
def get_match_mission_by_owner_service(match_id,player_id):
    return get_match_mission_by_owner_repo(
        match_id=match_id,
        player_id=player_id,
        )
#ERRO}
# DIFF: EASY

