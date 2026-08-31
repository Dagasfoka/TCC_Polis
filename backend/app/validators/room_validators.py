from dataclasses import dataclass


@dataclass
class RoomValidator:
    def not_exist(self,room_dict):
        if room_dict is None:
                raise Exception("Room não existe")
        return room_dict