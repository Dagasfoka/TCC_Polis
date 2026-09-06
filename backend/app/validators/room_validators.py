from dataclasses import dataclass


@dataclass
class RoomValidator:
    def not_exist(self,room_dict):
        if room_dict is None:
                raise Exception("Room não existe")
        return room_dict
    def player_can_start(self,player_id,room_dict):
        for p_id in room_dict['players']:
            if self.player_is_host(room_dict,p_id):
                if player_id != p_id:
                    raise Exception("Apenas o host pode iniciar")
        return player_id
    def player_is_duplicate(self,player_id,room_dict):
        if player_id in room_dict["players"]:
            return room_dict
    def max_players_room(self,room_dict):
        if len(room_dict['players']) >= 4:
            raise Exception ("A sala esta cheia")
        return room_dict
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
    def can_delete(self,room_dict,player_id):
        if self.player_is_host(room_dict,player_id):
            return room_dict
        raise Exception ("Somente o host pode deletar")
        #Tem que impedir o host de se deletar. Apesar de que na teoria nem vai ter esse botão.
    def player_is_host(self,room_dict,player_id):
        if room_dict['players'][player_id]['host'] == True:
            return True
        return False
    def four_players(self,room_dict):
        if len(room_dict['players']) != 4:
            raise Exception ("Não tem quatro jogadores")
        return True
