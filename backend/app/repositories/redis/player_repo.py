#Ligação do player com o redis
from json import dumps, loads

from backend.app.db.redis import redis_client
from backend.app.models.redis.player_model import Player
from backend.app.utils.ids import generate_player_id

### ERRO Mudar as validações para validators
#DIFF : VERY EASY

def save_player(username=None, party_id=None):
    player_id = generate_player_id()

    player = Player(
        player_id=player_id,
        match_id=None,
        party_id=party_id,
        username=username,
    )

    player_dict = player.to_dict()

    key = f"player:{player_id}"
    redis_client.set(key, dumps(player_dict))

    return player_dict

def get_player_repo(player_id):
    key = f"player:{player_id}"
    player_json = redis_client.get(key)

    if player_json:
        return loads(player_json)

    return None
def get_all_players():
    key = "player"
    redis_client.get(key)