from backend.app.repositories.db.territory_repo import TerritoryRepo
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
db: Session = Depends(get_db)
class TerritoryGateway:
    def __init__(self):
        self.db=db
        self.territory_repository=TerritoryRepo()
    def get_territory_by_id(self,target_territory_id):
        return self.territory_repository.get_territory_by_id(self.db,target_territory_id)