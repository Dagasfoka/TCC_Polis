# Criar jogador, nickname, recursos.
# Busca/salva salas temporárias no Redis.
from backend.app.repositories.redis.player_repo import get_player_repo, save_player


def create_player(username=None, party_id=None):
    player_dict=save_player(username=username, party_id=party_id)
    return player_dict
def get_player(player_id):
    return get_player_repo(player_id)