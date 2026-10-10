from backend.app.validators.match_validators import MatchValidator
from backend.app.gateways.match_gateways import MatchGateway
from backend.app.validators.player_validators import PlayerValidator
from backend.app.validators.match_territory_validator import MatchTerritoryValidator
from backend.app.factories.match_factory import MatchFactory

match_territory_validator=MatchTerritoryValidator()
match_factory=MatchFactory()
match_validator=MatchValidator()
match_gateway=MatchGateway()
player_validator=PlayerValidator()
def distribute_match_influence(match_id,player_id,distributed_influence,territory_id): #To fazendo esse so pra poder digitar e pensar sem afetar algo que alguem possivelmente ta mexendo
        match_dict=match_gateway.get_match(match_id)
        match_dict=match_validator.match_exist(match_dict)
        match_validator.verify_current_turn_player_id(match_dict,player_id)
        player=match_gateway.find_player(match_dict,player_id)
        player=player_validator.not_exist(player)
        match_influence=player['match_influence']
        match_influence=match_validator.verify_player_match_influence_is_not_below_zero(match_influence)
        territory=match_gateway.get_territory_by_id(match_dict,territory_id)
        territory=match_territory_validator.territory_exist(territory)
        distributed_influence=match_validator.verify_distributed_influence_is_on_limit(match_influence,distributed_influence)
        match_territory_validator.verify_territory_owner_id(territory,player_id)
        
        match_influence-=distributed_influence
        player['match_influence']=match_influence
        territory['current_influence']+=distributed_influence
        
        match_factory.update_match(match_dict)
        return match_dict