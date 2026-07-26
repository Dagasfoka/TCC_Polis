from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.db.mission import Mission


class MissionsRepository:
    def __init__(self, db:Session):
        self.db = db
    def get_all_missions(self) -> list[Mission]:
        return list(self.db.scalars(select(Mission)).all())

    def get_mission_by_id(self, mission_id: int) -> Mission | None:
        return self.db.get(Mission, mission_id)