from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.database.territory_model import Territory


def get_all_territories(db: Session) -> list[Territory]:
    return list(db.scalars(select(Territory)).all())


def get_territory_by_id(db: Session, territory_id: str) -> Territory | None:
    return db.get(Territory, territory_id)