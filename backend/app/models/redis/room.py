# Sala/lobby temporário.
class Room:
    def __init__(self, room_code: str,host_player_id:str):
        self.room_code = room_code
        self.players = []
        self.host_player_id = host_player_id
        self.status = "waiting"

    def to_dict(self):
        return {
            "room_code": self.room_code,
            "players": [p.to_dict() for p in self.players],
            "host_player_id": self.host_player_id,
            "status": self.status,
        }