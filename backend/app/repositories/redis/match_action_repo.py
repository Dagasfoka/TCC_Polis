from backend.app.factories.match_factory import MatchFactory
from backend.app.gateways.match_gateways import MatchGateway

class MatchActionRepo:

    def __init__(self):
        self.match_gateway = MatchGateway()
        self.match_factory = MatchFactory()

    def get_all_match_actions(self, match_id, action_type):
        match_dict = self.match_gateway.get_match(match_id)

        if match_dict is None:
            raise ValueError("Partida não encontrada.")

        return match_dict.get( f"{action_type}_actions",[],)

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
    ):
        match_dict = self.match_gateway.get_match(match_id)

        if match_dict is None:
            raise ValueError("Partida não encontrada.")

        match_dict["actions"] = actions

        self.match_factory.update_match(match_dict)

        return actions

    def update_match_action(
        self,
        match_id,
        updated_action,
    ):
        match_dict = self.match_gateway.get_match(match_id)

        if match_dict is None:
            raise ValueError("Partida não encontrada.")

        actions = match_dict.get("actions", [])

        for index, action in enumerate(actions):
            if action["action_id"] == updated_action["action_id"]:
                actions[index] = updated_action

                self.match_factory.update_match(match_dict)

                return updated_action

        raise ValueError("Ação não encontrada.")