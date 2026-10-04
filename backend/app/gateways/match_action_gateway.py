from backend.app.repositories.redis.match_action_repo import MatchActionRepo


class MatchActionGateway:

    def __init__(self):
        self.repository = MatchActionRepo()

    def get_all_match_actions(
        self,
        match_id: int,
        action_type: str,
    ):
        return self.repository.get_all_match_actions(
            match_id,
            action_type
        )

    def get_match_action_by_id(
        self,
        match_id: int,
        action_id: int,
        action_type: str
    ):
        return self.repository.get_match_action_by_id(
            match_id,
            action_id,
            action_type
        )

    def save_match_actions(
        self,
        match_id: int,
        actions: list,
        action_type: str
    ):
        return self.repository.save_match_actions(
            match_id,
            actions,
            action_type
        )

    def update_match_action(
        self,
        match_id: int,
        updated_action: dict,
        action_type: str
    ):
        return self.repository.update_match_action(
            match_id,
            updated_action,
            action_type
        )