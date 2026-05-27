from backend.app.models.redis.room_model import Room
from backend.app.utils.ids import generate_room_code

#import errado 

def build_room(host_player_id) -> Room:
    room_code = generate_room_code()
    return Room(room_code,host_player_id)