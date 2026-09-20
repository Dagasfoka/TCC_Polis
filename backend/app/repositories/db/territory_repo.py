from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.db.territory import Territory

class TerritoryRepo:
    def get_all_territories(self,db: Session) -> list[Territory]:
        return list(db.scalars(select(Territory)).all())


    def get_territory_by_id(self,db: Session, territory_id: str) -> Territory | None:
        return db.get(Territory, territory_id)