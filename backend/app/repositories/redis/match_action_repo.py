from backend.app.factories.match_factory import MatchFactory
from backend.app.gateways.match_gateways import MatchGateway

class MatchActionRepo:

    def __init__(self):
        self.match_gateway = MatchGateway()
        self.match_factory = MatchFactory()

    def get_all_match_actions(self, match_id, action_type):
        match_dict = self.match_gateway.get_match(match_id)
        if action_type == "attack":
            active_list = match_dict['activate_attack_actions_list'][-2:]
        else:
            active_list = match_dict['activate_defense_actions_list'][-2:]
        return match_dict.get( f"{action_type}_actions{active_list}",[],)

    def get_match_action_by_id(
        self,
        match_id,
        action_id,
        action_type
    ):
        for action in self.get_all_match_actions(match_id,action_type):
            if action["action_id"] == action_id:
                return action

        return None

    def save_match_actions(
        self,
        match_id,
        actions,
        action_type,
        active_action_list,
    ):
        match_dict = self.match_gateway.get_match(match_id)
        active_action_list = active_action_list[-2:]
    
        match_dict[f"{action_type}_actions{active_action_list}"] = actions

        self.match_factory.update_match(match_dict)

        return actions