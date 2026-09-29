from backend.app.repositories.redis.player_repo import PlayerRepo
class PlayerFactory:
    def __init__(self) -> None:
        self.player_repository=PlayerRepo()
    def create_player(self,username,party_id=None):
        return self.player_repository.create_player(username,party_id)