from json import dumps, loads

from backend.app.models.redis.room import Room
from backend.app.models.redis.room_player import RoomPlayer
from backend.app.utils.ids import generate_room_code
from backend.app.db.redis import redis_client


class RoomRepo:

    def __init__(self):
        pass
    def get_room(self, room_code) -> dict | None:
        key = f"room:{room_code}"
        room_JSON = redis_client.get(key)
        if room_JSON is not None:
            return loads(room_JSON)
        return None
    def update_room(self, room_dict):
        room_JSON = dumps(room_dict)
        key = f"room:{room_dict['room_code']}"
        redis_client.set(key, room_JSON)
        return room_dict
    def create_room(self, host_player_id, is_private=False):
        room_code = generate_room_code()
        room_player = self.create_room_player(
            player_id=host_player_id,
            host=True,
        )
        room = Room(
            room_code=room_code,
            is_private=is_private
        )
        room_dict = room.to_dict()
        room_dict["players"][room_player["player_id"]] = {
            "ready": room_player["ready"],
            "host": room_player["host"],
        }
        return self.update_room(room_dict)
    def create_room_player(
        self,
        player_id,
        ready=False,
        host=False
    ):
        room_player = RoomPlayer(
            player_id=player_id,
            ready=ready,
            host=host,
        )
        return room_player
    def get_public_rooms(self):
        public_rooms = []
        # Procura todas as chaves room:*
        for key in redis_client.scan_iter("room:*"):
            room_JSON = redis_client.get(key)
            if room_JSON is None:
                continue
            room = loads(room_JSON)
            # salas antigas podem não possuir is_private
            is_private = room.get("is_private", False)
            # sala privada não entra no matchmaking
            if is_private:
                continue
            # partida já começou
            if room.get("status") == "in_game":
                continue
            # sala cheia
            if len(room.get("players", {})) >= 4:
                continue
            public_rooms.append(room)
        return public_rooms
    def delete_room(self, room_code):
        key = f"room:{room_code}"
        return redis_client.delete(key)