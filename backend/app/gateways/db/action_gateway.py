from backend.app.repositories.db.action_repo import ActionRepo
class ActionGateway:
    def __init__(self) -> None:
        self.action_repository=ActionRepo()

    def get_all_action(self):
        return self.action_repository.get_all_action()
    
    def get_actions_by_type(self,action_type: str):
        return self.action_repository.get_actions_by_type(action_type)