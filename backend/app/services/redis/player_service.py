# Criar jogador, nickname, recursos.
# Busca/salva salas temporárias no Redis.
from backend.app.gateways.player_gateways import PlayerGateway
from backend.app.factories.player_factory import PlayerFactory

player_gateway= PlayerGateway()
player_factory=PlayerFactory()
def create_player(username=None, party_id=None):
    player_dict=player_factory.create_player(username=username, party_id=party_id)
    return player_dict
def get_player(player_id):
    return player_gateway.get_player(player_id)