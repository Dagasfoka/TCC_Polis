#Ligação do player com o redis
from json import dumps, loads

from backend.app.db.redis import redis_client
from backend.app.models.redis.player import Player
from backend.app.utils.ids import generate_player_id, generate_player_token

class PlayerRepo:
    def __init__(self) -> None:
        pass
    def create_player(self,username, party_id=None):
        player_id = generate_player_id()
        player_token = generate_player_token()
        player_dict = Player.create_dict(
            player_id=player_id,
            match_id=None,
            party_id=None,
            player_token = player_token,
            username=username
        )

        key = f"player:{player_id}"
        redis_client.set(key, dumps(player_dict))

        key = f"player_token:{player_token}"
        redis_client.set(key,player_id)

        return {
             **player_dict,
        }
    def get_player(self, player_id):
        key = f"player:{player_id}"
        player_json = redis_client.get(key)

        if isinstance(player_json, (str, bytes)):
            return loads(player_json)
        return None
    def get_player_repo_by_token(self,player_token):

        key = f"player_token:{player_token}"

        player_id = redis_client.get(key)

        if not player_id:
            return None

        return self.get_player(player_id)

    def delete_player(self, player_id):
        player = self.get_player(player_id)
        if player is None:
            return
        player_token = player.get("player_token")
        
        redis_client.delete(f"player:{player_id}")
        
        if player_token:
            redis_client.delete(f"player_token:{player_token}")