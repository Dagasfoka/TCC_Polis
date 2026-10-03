from backend.app.repositories.db.territory_repo import TerritoryRepo
from backend.app.db.database import SessionLocal
db = SessionLocal()

class MatchTerritoryValidator:
    def __init__(self) -> None:
        self.territory_repo = TerritoryRepo()

    def frontier_verify(
        self,
        target_territory_id,
        player_id,
        match_territories,
    ):
        target_territory = self.territory_repo.get_territory_by_id(
            db,
            target_territory_id,
        )

        target_territory = self.territory_exist(target_territory)

        target_territory_frontiers = target_territory.frontiers

        player_territories = []

        for territory in match_territories:
            if territory["owner_id"] == player_id:
                player_territories.append(territory["territory_id"])

        if not any(
            territory_id in target_territory_frontiers
            for territory_id in player_territories
        ):
            raise Exception("Você não possui fronteiras com esse território")

        return True
    #_______SIMPLES
    def territory_exist(self, territory):
        if territory is None:
            raise Exception("Território não existe")
        return territory
    def verify_territory_owner_id(self,target,player_id, action_type):
        if target["owner_id"] == player_id:
            if action_type == "attack":
                raise ValueError("Você já controla esse território, não poderá atacar ele.")
            return target
        if action_type == "defense":
            raise ValueError("Você não controla esse território, não poderá defender ele.")
        return target