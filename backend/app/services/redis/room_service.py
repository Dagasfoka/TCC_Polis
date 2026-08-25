# Criar sala, entrar, sair, iniciar partida.]
from backend.app.factories.room_factory import RoomFactory
from backend.app.repositories.redis.player_repo import get_player_repo
from backend.app.gateways.room_gateways import RoomGateway
from backend.app.services.redis.match_service import create_match


def create_room(host_player_id:str) -> dict:
    room_factory=RoomFactory()
    room_dict=room_factory.create_room(host_player_id)
    return room_dict

def join_room(player_id, room_code):
    room_gateway=RoomGateway()
    room_factory=RoomFactory()
    room_dict = room_gateway.get_room(room_code)
    print("Saida:",room_dict)
    if room_dict is None:
        raise Exception("Room não existe")

    player = get_player_repo(player_id)

    if player is None:
        raise Exception("Player não existe")

    # evitar duplicado
    if player["player_id"] in room_dict["players"]:
        return room_dict
    room_player=room_factory.create_room_player(player_id)
    room_dict["players"][room_player['player_id']]={
        'ready':room_player['ready'],
        'host':room_player['host'],
        }

    room_factory.update_room(room_dict)

    return room_dict

def get_room(room_code):
    room_gateway=RoomGateway()
    return room_gateway.get_room(room_code)

def start_game(db,room_code,redis_client, player_id):
    room_gateway=RoomGateway()
    room_factory=RoomFactory()
    room_dict = get_room(room_code)
    if room_dict is None:
        raise Exception("A sala não foi encontrada")
    if player_id != room_dict["host_player_id"]:
        raise Exception("Apenas o host pode iniciar")

    match = create_match(db=db,redis_client=redis_client,room_code=room_code)

    room_dict["status"] = "in_game"
    room_factory.update_room(room_dict)

    return match