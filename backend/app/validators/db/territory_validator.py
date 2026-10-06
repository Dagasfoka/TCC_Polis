class TerritoryValidator:
    def territory_exist(self,territory):
        if territory is not None:
            return territory
        raise ValueError("Território não encontrado")