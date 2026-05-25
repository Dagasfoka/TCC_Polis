# Criar sala, entrar, sair, iniciar partida.]
from backend.app.factories.redis.room_factory import build_room
from backend.app.repositories.redis.player_repo import get_player_repo
from backend.app.repositories.redis.room_repo import get_room_repo, save_room
from backend.app.services.redis.match_service import create_match
#ERROR Não pode importar REPO

def create_room(host_player_id:str) -> dict:
    room = build_room(host_player_id)
    room_dict = room.to_dict()
    save_room(room_dict)
    return room_dict

def join_room(player_id, room_code):
    room_dict = get_room(room_code)

    if room_dict is None:
        raise Exception("Room não existe")

    player = get_player_repo(player_id)

    if player is None:
        raise Exception("Player não existe")

    # evitar duplicado
    if any(p["player_id"] == player["player_id"] for p in room_dict["players"]):
        return room_dict

    room_dict["players"].append(player)

    save_room(room_dict)

    return room_dict

def get_room(room_code):
    return get_room_repo(room_code)

def start_game(db,room_code, player_id):
    room_dict = get_room(room_code)

    if player_id != room_dict["host_player_id"]:
        raise Exception("Apenas o host pode iniciar")

    match = create_match(db,room_code)

    room_dict["status"] = "in_game"
    save_room(room_dict)

    return match