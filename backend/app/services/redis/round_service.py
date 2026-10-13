from backend.app.validators.match_validators import MatchValidator
from backend.app.gateways.match_gateways import MatchGateway
from backend.app.validators.player_validators import PlayerValidator
from backend.app.validators.match_territory_validator import MatchTerritoryValidator
from backend.app.factories.match_factory import MatchFactory
from backend.app.services.redis.action_service import (
    get_match_attack_actions,
    get_match_defense_actions,
    distribute_actions
)
import random
class RoundService:
        def __init__(self) -> None:
                self.match_territory_validator=MatchTerritoryValidator()
                self.match_factory=MatchFactory()
                self.match_validator=MatchValidator()
                self.match_gateway=MatchGateway()
                self.player_validator=PlayerValidator()
        def distribute_match_influence(self,match_id,player_id,distributed_influence,territory_id): #To fazendo esse so pra poder digitar e pensar sem afetar algo que alguem possivelmente ta mexendo
                match_dict=self.match_gateway.get_match(match_id)
                match_dict=self.match_validator.match_exist(match_dict)
                self.match_validator.verify_current_turn_player_id(match_dict,player_id)
                player=self.match_gateway.find_player(match_dict,player_id)
                player=self.player_validator.not_exist(player)
                match_influence=player['match_influence']
                match_influence=self.match_validator.verify_player_match_influence_is_not_below_zero(match_influence)
                territory=self.match_gateway.get_territory_by_id(match_dict,territory_id)
                territory=self.match_territory_validator.territory_exist(territory)
                distributed_influence=self.match_validator.verify_distributed_influence_is_on_limit(match_influence,distributed_influence)
                self.match_territory_validator.verify_territory_owner_id(territory,player_id)
                
                match_influence-=distributed_influence
                player['match_influence']=match_influence
                territory['current_influence']+=distributed_influence
                
                self.match_factory.update_match(match_dict)
                return match_dict
        def skip_turn_by_money_insufficient(self,match,action_result):
                skipped_player_id=match['current_turn_player_id']
                self.match_factory.advance_turn(match)
                return {
                "match": match,
                "result": {
                **action_result,
                "next_turn_player_id": match["current_turn_player_id"],
                "round": match["round"],
                "winner_id": match.get("winner_id"),
                "status": match["status"],
                "skipped_player_id": skipped_player_id,
                        },
                }
        def initial_distribute_actions(self,match):
                match_id=match['match_id']
                available_attack_actions = get_match_defense_actions(match_id)
                available_defenses_actions = get_match_attack_actions(match_id)
                
                available_attack_actions = list(available_attack_actions)
                random.shuffle(available_attack_actions)

                available_actions = distribute_actions(available_attack_actions)

                match["round_attack_actions"] = available_actions
                
                available_defenses_actions = list(available_defenses_actions)
                random.shuffle(available_defenses_actions)

                available_actions = distribute_actions(available_defenses_actions)

                match["round_defense_actions"] = available_actions
                return match