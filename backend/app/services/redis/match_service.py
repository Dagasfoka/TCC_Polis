# Ataque, defesa, turno, vitória, mapa.
from backend.app.factories.create_match_factory import (
    build_initial_match_state,
)
from backend.app.repositories.redis.match_repo import get_match_state, save_match_state

from backend.app.gateways.room_gateways import RoomGateway
from backend.app.validators.room_validators import RoomValidator

from backend.app.factories.match_mission_factory import MatchMissionFactory
from backend.app.factories.match_question_factory import MatchQuestionFactory
from backend.app.factories.match_territory_factory import MatchTerritory
def create_match(db,room_code):
    #gateways
    room_gateway=RoomGateway()
    #factories
    match_mission_factory= MatchMissionFactory()
    match_question_factory=MatchQuestionFactory(db)
    match_territory_factory=MatchTerritory()
    #validators
    room_validator=RoomValidator()
    
    room_dict=room_gateway.get_room(room_code)
    
    room_validator.not_exist(room_dict)

    
    match_state=build_initial_match_state(db,room_dict)
    match_dict = match_state.to_dict()
    
    match_dict['players']=match_territory_factory.distribute_territories(match_dict['players'],match_dict['territories'])
    match_dict["players"]=match_question_factory.distribute_questions(match_dict['players'])
    match_dict['missions']=match_mission_factory.distribute_match_missions(
        match_id=match_dict["match_id"],
        players=match_dict['players'],
        db= db,
    )
    save_match_state(match_dict)
    return match_dict

def get_match(match_id):
    return get_match_state(match_id)