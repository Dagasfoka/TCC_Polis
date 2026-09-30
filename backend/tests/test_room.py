from backend.tests.models.room_test import RoomPlayer,Room
from backend.tests.models.player_test import Player
player=Player("asd",1,1)
player_dict=player.to_dict()

room_player= RoomPlayer(player_id=player_dict['player_id'],ready=False,host=True)
room=Room("sad")
room.players[player.player_id] = {
    'ready':room_player['ready'],
    'host':room_player['host'],
    }

print(room)