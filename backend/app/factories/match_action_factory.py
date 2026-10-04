from backend.app.gateways.match_action_gateway import MatchActionGateway


class MatchActionFactory:

    def __init__(self):
        self.gateway = MatchActionGateway()

    def get_actions_by_type(
        self,
        match_id: int,
        action_type: str,
    ):
        return self.gateway.get_all_match_actions(
            match_id,
            action_type,
        )

    def get_action_by_id(
        self,
        match_id: int,
        action_id: int,
        action_type: str,
    ):
        return self.gateway.get_match_action_by_id(
            match_id,
            action_id,
            action_type,
        )