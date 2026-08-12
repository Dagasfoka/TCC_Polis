from backend.tests.models.room_test import RoomPlayer,Room
from backend.tests.models.player_test import Player
player=Player("asd",1,1)
player_dict=player.to_dict()

room_player= RoomPlayer(player=player_dict,ready=False,host=True)
room=Room("sad")
room.players[player.player_id] = room_player

print(room)