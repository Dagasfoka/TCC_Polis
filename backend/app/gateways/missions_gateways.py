from sqlalchemy.orm import Session

from backend.app.repositories.db.mission_repo import MissionsRepository

#from backend.app.validators.missions_validators import *

class MissionsGateway:
    def __init__(self, db: Session):
        self.missions_repository = MissionsRepository(db)
    def get_all_missions(self):
        return self.missions_repository.get_all_missions()