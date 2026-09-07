from backend.app.repositories.redis.room_repo import RoomRepo
class RoomGateway:
    def __init__(self) -> None:
        self.room_repository=RoomRepo()
    def get_room(self,roomcode):
        return self.room_repository.get_room(roomcode)