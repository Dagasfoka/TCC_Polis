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