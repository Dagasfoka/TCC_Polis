class MatchTerritory:
    def __init__(self,match_id, territory_id, base_influence, name, region):
        self.match_id=match_id
        self.territory_id=territory_id
        self.base_influence=base_influence
        self.current_influence=base_influence
        self.owner_id=None 
        self.name=name
        self.region=region
    def to_dict(self):
        return {
            "match_id": self.match_id,
            "territory_id": self.territory_id,
            "base_influence": self.base_influence,
            "current_influence": self.current_influence,
            "owner_id": self.owner_id,
            "name": self.name,
            "region": self.region,
        }