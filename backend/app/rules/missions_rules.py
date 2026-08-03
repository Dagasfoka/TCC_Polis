import random
from backend.app.validators.missions_validators import *
class MissionsRules:
    def __init__(self,missions) -> None:
        self.missions=missions
    def choose_missions(self, quantity_players):
        if len(self.missions) < quantity_players:
            raise ValueError("Não há missões suficientes para todos os jogadores.")
        return random.sample(self.missions, quantity_players)
