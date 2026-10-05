from backend.app.repositories.db.territory_repo import TerritoryRepo
class TerritoryGateway:
    def __init__(self):
        self.territory_repository=TerritoryRepo()
    def get_territory_by_id(self,db,target_territory_id):
        return self.territory_repository.get_territory_by_id(db,target_territory_id)