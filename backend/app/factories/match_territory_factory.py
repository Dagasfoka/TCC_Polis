import random
class MatchTerritory:
    def __init__(self) -> None:
        pass
    
    def distribute_territories(self,players,territories):
        random.shuffle(territories)
        for index, territory in enumerate(territories):
            player = players[index % len(players)]
            territory["owner_id"] = player["player_id"]

        return players