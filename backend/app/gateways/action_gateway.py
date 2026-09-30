from backend.app.repositories.db.action_repo import ActionRepo
class ActionGateway:
    def __init__(self) -> None:
        self.action_repository=ActionRepo()
    def list_action_by_type(self,action_type: str):
        return self.action_repository.list_options_by_action(action_type)
    def get_action_by_id(self,action_id: str):
        return self.action_repository.get_option_by_id(action_id)