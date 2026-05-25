from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.database.mission_model import Mission


def get_all_missions(db: Session) -> list[Mission]:
    return list(db.scalars(select(Mission)).all())

def get_mission_by_id(db: Session, mission_id: int) -> Mission | None:
    return db.get(Mission, mission_id)