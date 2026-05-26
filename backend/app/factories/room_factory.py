from backend.app.models.room import Room
from backend.app.utils.ids import generate_room_code


def build_room(host_player_id) -> Room:
    room_code = generate_room_code()
    return Room(room_code,host_player_id)