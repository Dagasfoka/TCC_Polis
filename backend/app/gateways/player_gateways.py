from backend.app.repositories.redis.player_repo import  PlayerRepo,get_player_repo
class PlayerGateway:
    def __init__(self) -> None:
        self.player_repo=PlayerRepo
    def get_players(self, player_ids):
        players = []

        for player_id in player_ids:
            player = get_player_repo(player_id)
            players.append(player)

        return players
    """
    def get_players(self, player_ids):
        players = []

        for player_id in player_ids:
            player = self.player_repo.get_player(player_id)
            players.append(player)

        return players
        """