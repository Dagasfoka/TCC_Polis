from backend.app.models.db.action import Action
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.db.database import SessionLocal

class ActionRepo:

    def __init__(self):
            self.db = SessionLocal()
            
    def get_all_action(self,db: Session) -> list[Action]:
            return list(db.scalars(select(Action)).all())
    
    
    def get_actions_by_type(self,db: Session, action_type: str) -> Action | None:
        actions = select(Action).where(Action.action_type == action_type)
        return list(db.scalars(actions).all())
