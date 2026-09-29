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
        room_json = redis_client.get(key)

        if room_json is not None:
            return loads(room_json)

        return None

    def update_room(self, room_dict):
        room_json = dumps(room_dict)
        key = f"room:{room_dict['room_code']}"

        redis_client.set(key, room_json)

        return room_dict

    def create_room(
        self,
        host_player_id,
        is_private=False
    ):
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

        room_dict["players"][room_player.player_id] = {
            "ready": room_player.ready,
            "host": room_player.host,
            "party_id": room_player.party_id,
        }

        return self.update_room(room_dict)

    def create_room_player(
        self,
        player_id,
        ready=False,
        host=False,
        party_id=None,
    ):
        return RoomPlayer(
            player_id=player_id,
            ready=ready,
            host=host,
            party_id=party_id,
        )

    def get_public_rooms(self):
        public_rooms = []

        for key in redis_client.scan_iter("room:*"):
            room_json = redis_client.get(key)

            if room_json is None:
                continue

            room = loads(room_json)

            if room.get("is_private", False):
                continue

            if room.get("status") == "in_game":
                continue

            if len(room.get("players", {})) >= 4:
                continue

            public_rooms.append(room)

        return public_rooms

    def delete_room(self, room_code):
        key = f"room:{room_code}"

        return redis_client.delete(key)