from dataclasses import dataclass

@dataclass
class PlayerValidator:
    def not_exist(self,player):
        if player is None:
            raise Exception("Player não existe")
        return player