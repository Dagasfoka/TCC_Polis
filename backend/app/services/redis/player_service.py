from backend.app.gateways.player_gateways import PlayerGateway
from backend.app.factories.player_factory import PlayerFactory

from backend.app.gateways.db.user_gateways import UsersGateway
from backend.app.factories.user_factory import UserFactory

from backend.app.validators.user_validators import UserValidator


player_gateway = PlayerGateway()
player_factory = PlayerFactory()

user_gateway = UsersGateway()
user_factory = UserFactory()
user_validator = UserValidator()

def create_player(username=None,party_id=None):
    return player_factory.create_player(username=username, party_id=party_id)

def create_user_player(user_id):
    user = user_gateway.get_user_by_id(user_id)
    user = user_validator.not_exist(user)
    existing_player = None
    if user.player_id is not None:
        existing_player = (player_gateway.get_player(user.player_id))
    user_validator.user_can_create_player(user,existing_player)
    #Existe player_id no SQL,
    # mas Player já não existe no Redis.
    if (user.player_id is not None and existing_player is None):
        user_factory.update_player_id(user.user_id, None)
    player = player_factory.create_player(username=user.username)
    user_factory.update_player_id(user.user_id, player["player_id"])
    return player

def get_player(player_id):
    return player_gateway.get_player(player_id)

def delete_user_player(user_id):
    user = user_gateway.get_user_by_id(user_id)
    user = user_validator.not_exist(user)
    if user.player_id is None:
        return user
    player_factory.delete_player(user.player_id)
    user_factory.update_player_id(user.user_id, None)
    return user
def delete_player(player_id):
    return player_factory.delete_player(
        player_id
    )