# Busca/salva salas temporárias no Redis.
from json import dumps, loads
from backend.app.models.redis.room import Room
from backend.app.models.redis.room_player import RoomPlayer
from backend.app.utils.ids import generate_room_code
from backend.app.db.redis import redis_client

class RoomRepo:
    def __init__(self):
        pass
    def get_room(self,room_code) -> dict | None:
        key = f"room:{room_code}"
        room_JSON=redis_client.get(key)
        if room_JSON is not None:
            return loads(room_JSON)
        return None
    def update_room(self,room_dict):
        room_JSON=  dumps(room_dict)
        key = f"room:{room_dict['room_code']}"
        redis_client.set(key,room_JSON)
        return room_dict
    def create_room(self,host_player_id):
        room_code = generate_room_code()
        room_player=self.create_room_player(
            player_id=host_player_id,
            host=True,
            )
        room=Room(room_code)
        room_dict=room.to_dict()
        room_dict['players'][room_player['player_id']]={
            'ready':room_player['ready'],
            'host':room_player['host'],
            }
        return self.update_room(room_dict)
    def create_room_player(self,player_id,ready=False,host=False):
       room_player= RoomPlayer(
                    player_id=player_id,
                    ready=ready,
                    host=host,
                    )
       return room_player