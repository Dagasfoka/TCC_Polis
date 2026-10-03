from backend.app.models.db.action import Action
from sqlalchemy import select
from backend.app.db.database import SessionLocal

class ActionRepo:

    def __init__(self):
            self.db = SessionLocal()

    def get_all_action(self) -> list[Action]:
            return list(self.db.scalars(select(Action)).all())
    
    def get_action_by_id(self, action_id) -> Action:
        return self.db.get(Action, action_id)
    
    def get_actions_by_type(self, action_type: str) -> Action | None:
        actions = select(Action).where(Action.action_type == action_type)
        return list(self.db.scalars(actions).all())
