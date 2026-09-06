# Criar sala, entrar, sair, iniciar partida.]
from backend.app.factories.room_factory import RoomFactory
from backend.app.gateways.room_gateways import RoomGateway
from backend.app.validators.room_validators import RoomValidator
from backend.app.validators.player_validators import PlayerValidator
from backend.app.repositories.redis.player_repo import get_player_repo
from backend.app.services.redis.match_service import create_match


def create_room(host_player_id:str) -> dict:
    room_factory=RoomFactory()
    room_validator=RoomValidator()
    room_dict=room_factory.create_room(host_player_id)
    room_dict=room_validator.not_exist(room_dict)
    return room_dict

def join_room(player_id, room_code):
    room_validator=RoomValidator()
    room_gateway=RoomGateway()
    room_factory=RoomFactory()

    player_validator=PlayerValidator()

    room_dict = room_gateway.get_room(room_code)
       
    room_dict = room_validator.not_exist(room_dict)
    room_dict = room_validator.max_players_room(room_dict)
    
    player = get_player_repo(player_id)

    player=player_validator.not_exist(player)
    player_id=player["player_id"]
    # evitar duplicado
    room_validator.player_is_duplicate(player_id,room_dict)

    room_player=room_factory.create_room_player(player_id)
    # colocar dentro do factories?
    room_dict["players"][room_player['player_id']]={
        'ready':room_player['ready'],
        'host':room_player['host'],
        }
    #____
    room_factory.update_room(room_dict)

    return room_dict

def get_room(room_code):
    room_gateway=RoomGateway()
    return room_gateway.get_room(room_code)

def start_game(db,room_code,redis_client, player_id):
    room_gateway=RoomGateway()
    room_factory=RoomFactory()
    room_validator=RoomValidator()

    room_dict = room_gateway.get_room(room_code)

    room_dict=room_validator.not_exist(room_dict)
    player_id= room_validator.player_can_start(player_id,room_dict)
    if (room_validator.ready_to_start(room_dict)):
        match = create_match(db=db,redis_client=redis_client,room_code=room_code)

        room_dict["status"] = "in_game"
        room_factory.update_room(room_dict)

        return match
    raise Exception ("Sala não criada")
def put_ready(room_code,player_id):
    room_gateway=RoomGateway()
    room_factory=RoomFactory()
    room_validator=RoomValidator()
    
    player_validator=PlayerValidator()
    
    room_dict = room_gateway.get_room(room_code)
    room_dict=room_validator.not_exist(room_dict)

    player = get_player_repo(player_id)
    player=player_validator.not_exist(player)
    player_id=player["player_id"]
    room_factory.put_ready(room_dict,player_id)
    room_factory.update_room(room_dict)
    return room_dict
def delete_player(room_code,host_id,player_id):
    room_gateway=RoomGateway()
    room_factory=RoomFactory()
    room_validator=RoomValidator()
    
    player_validator=PlayerValidator()
    player = get_player_repo(player_id)
    player=player_validator.not_exist(player)
    player_id=player["player_id"]    
    
    room_dict = room_gateway.get_room(room_code)
    
    room_dict=room_validator.not_exist(room_dict)
    room_dict=room_validator.can_delete(room_dict,host_id)
    room_dict=room_factory.delete_player(room_dict,player_id)
    room_factory.update_room(room_dict)
    return room_dict
        