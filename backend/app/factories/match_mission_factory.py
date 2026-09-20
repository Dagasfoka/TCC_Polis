from email import contentmanager
import random


from backend.app.repositories.redis.match_mission_repo import MatchMissionRepo

from backend.app.gateways.missions_gateways import MissionsGateway

import random 
class MatchMissionFactory:
    def __init__(self):
        self.match_mission_repo=MatchMissionRepo()
    def distribute_match_missions(self,match_id, players,db):
        missions_gateway=MissionsGateway(db=db)
        
        missions=missions_gateway.get_all_missions()


        chosen_missions=self.choose_missions(quantity_players=len(players),missions=missions)

        #validator
        if len(players) != len(chosen_missions):
            raise ValueError("A quantidade de players precisa ser igual à quantidade de missões.")

        match_missions = []

        for player, mission in zip(players, chosen_missions):
            content = mission.content.copy()
            if mission.type == "destruction":
                content["destruction"] = self.choose_destruction_target(
                    players=players,
                    owner_id=player["player_id"],
                )
                mission.content=content
            match_mission= self.create_match_mission(
                match_id=match_id,
                mission_id=mission.mission_id,
                type=mission.type,
                content=mission.content,
                owner_id=player['player_id'],
                )
            
            match_missions.append(match_mission)
            
        return match_missions
    def choose_missions( self,missions, quantity_players):
            if len(missions) < quantity_players:
                raise ValueError("Não há missões suficientes para todos os jogadores.")
            return random.sample(missions, quantity_players)
    def choose_destruction_target(self,players, owner_id):
        possible_targets = [
            player["player_id"]
            for player in players
            if player["player_id"] != owner_id
        ]

        if not possible_targets:
            raise ValueError("Não há alvo possível para missão de destruição.")

        return random.choice(possible_targets)

    
    def create_match_mission(self,match_id,mission_id,type,content,owner_id):
        #_______________________________ validator
        if match_id is None:
            raise ValueError("Partida não encontrada.")
        #_______________________________ 
        match_mission_dict=self.match_mission_repo.create_match_mission(
            match_id=match_id,
            mission_id=mission_id,
            type=type,
            content=content,
            owner_id=owner_id,
            )
        return match_mission_dict