# Ataque, defesa, turno, vitória, mapa.
from backend.app.factories.match_factory import MatchFactory
from backend.app.gateways.match_gateways import MatchGateway

from backend.app.gateways.questions_gateways import QuestionGateways
from backend.app.gateways.room_gateways import RoomGateway
from backend.app.validators.room_validators import RoomValidator

from backend.app.factories.match_mission_factory import MatchMissionFactory
from backend.app.factories.match_question_factory import MatchQuestionFactory
from backend.app.factories.match_territory_factory import MatchTerritoryFactory
class MatchService:
    def __init__(self) -> None:
        self.match_factory=MatchFactory()
        self.match_gateway=MatchGateway()
    def create_match(self,db,room_code):
        #gateways
        room_gateway=RoomGateway()
        #factories
        match_mission_factory= MatchMissionFactory()
        question_gateways=QuestionGateways(db)
        match_territory_factory=MatchTerritoryFactory()
        #validators
        room_validator=RoomValidator()
        
        room_dict=room_gateway.get_room(room_code)
        
        room_validator.not_exist(room_dict)

        
        match_dict=self.match_factory.build_initial_match_state(
            db=db,
            room_dict=room_dict,
        )
        
        match_dict['players']=match_territory_factory.distribute_territories(match_dict['players'],match_dict['territories'])
        match_dict["questions_1"]=question_gateways.get_all_questions()
        match_dict["activate_questions_list"]="questions_1"
        match_dict['missions']=match_mission_factory.distribute_match_missions(
            match_id=match_dict["match_id"],
            players=match_dict['players'],
            db= db,
        )
        self.match_factory.update_match(match_dict)
        return match_dict

    def get_match(self,match_id):
        return self.match_gateway.get_match(match_id)