# Ataque, defesa, turno, vitória, mapa.

from backend.app.rules.match_rules import distribute_initial_territories_missions_questions

from backend.app.factories.create_match_factory import (
    build_initial_match_state,
)
from backend.app.repositories.redis.match_repo import get_match_state, save_match_state
from backend.app.gateways.room_gateways import RoomGateway

def create_match(db,redis_client,room_code):
    room_gateway=RoomGateway()
    room_dict=room_gateway.get_room(room_code)
    
    if room_dict is None:
        raise ValueError("Sala não encontrada")

    if not room_dict["players"]:
        raise ValueError("Sala sem jogadores")


    
    match_state=build_initial_match_state(db,room_dict)
    match_state_dict = match_state.to_dict()
    match_state_dict=distribute_initial_territories_missions_questions(
        db=db,
        redis_client=redis_client,
        match_state_dict=match_state_dict
    )
    save_match_state(match_state_dict)
    return match_state_dict

def get_match(match_id):
    return get_match_state(match_id)