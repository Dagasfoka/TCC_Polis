from backend.app.repositories.redis.player_repo import  PlayerRepo
class PlayerGateway:
    def __init__(self) -> None:
        self.player_repository=PlayerRepo()
    def get_players(self, player_ids):
        players = []
        for player_id in player_ids:
            player = self.get_player(player_id)
            players.append(player)

        return players
    def get_player(self,player_id):
        return self.player_repository.get_player(player_id)