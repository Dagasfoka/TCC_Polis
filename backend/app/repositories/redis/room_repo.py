# Busca/salva salas temporárias no Redis.
from json import dumps, loads

from backend.app.db.redis import redis_client


def get_room_repo(room_code) -> dict | None:
    key = f"room:{room_code}"
    room_JSON=redis_client.get(key)
    if room_JSON is not None:
        return loads(room_JSON)
    return None
def save_room(room_dict):
    room_JSON=  dumps(room_dict)
    key = f"room:{room_dict['room_code']}"
    redis_client.set(key,room_JSON)