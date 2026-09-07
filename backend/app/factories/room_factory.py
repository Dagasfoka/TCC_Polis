from os import read

from backend.app.repositories.redis.room_repo import RoomRepo
from backend.app.models.redis.room import Room


class RoomFactory:
    def __init__(self) -> None:
       self.room_repository=RoomRepo()
    def update_room(self,room_dict):
        self.room_repository.update_room(room_dict)
        print("Upado")
    def create_room(self,host_player_id):
        return self.room_repository.create_room(host_player_id)
    def create_room_player(self,player_id):
        return self.room_repository.create_room_player(player_id)
    def put_ready(self,room_dict,player_id):
        for p_id in room_dict['players']:
            if p_id==player_id:
                room_dict['players'][player_id]['ready']=True
        return room_dict
        #Tem que atualizar a room, essa function so coloca ready
        # Frontend tem que fazer o host não ver esse botão.
    def delete_player(self, room_dict, player_id):
        del room_dict["players"][player_id]
        return room_dict