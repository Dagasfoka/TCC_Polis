from dataclasses import dataclass


@dataclass
class RoomValidator:
    def not_exist(self,room_dict):
        if room_dict is None:
                raise Exception("Room não existe")
        return room_dict
    def player_can_start(self,player_id,room_dict):
        if player_id != room_dict["host_player_id"]:
            raise Exception("Apenas o host pode iniciar")
        return player_id
    def player_is_duplicate(self,player_id,room_dict):
        if player_id in room_dict["players"]:
            return room_dict
    def four_players(self,room_dict):
        if len(room_dict['players']) != 4:
            return False
        return True
    def ready_to_start(self, room_dict) -> bool:
        self.four_players(room_dict)
        players=room_dict['players']
        All_ready=False
        for player_id in players:
            if players[player_id]['host'] is True:
                continue
            ready=players[player_id]["ready"]
            if ready is not True:
                return All_ready
        All_ready=True
        return All_ready
