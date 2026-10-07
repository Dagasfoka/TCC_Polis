from backend.app.factories.match_territory_factory import MatchTerritoryFactory
from backend.app.repositories.redis.match_repo import MatchRepo
from backend.app.repositories.db.territory_repo import TerritoryRepo
from backend.app.gateways.player_gateways import PlayerGateway
from backend.app.models.redis.match import Match
from backend.app.factories.action_factory import INITIAL_MONEY,INITIAL_INFLUENCE

class MatchFactory:
    def __init__(self) -> None:
        self.match_repository=MatchRepo()
        self.territory_repo=TerritoryRepo()
        self.player_gateway=PlayerGateway()
        self.match_territory_factory= MatchTerritoryFactory()
    def update_match(self,match_dict):
        return self.match_repository.update_match(match_dict)
    def build_initial_match_state(self, db, room_dict) -> dict:
        territories = self.territory_repo.get_all_territories(db)
        match_territories = []
        match_id = self.match_repository.generate_match_id()

        for territory_data in territories:
            match_territory = self.match_territory_factory.build_match_territory(
                match_id,
                territory_data,
            )
            match_territories.append(match_territory)

        players_ids = room_dict["players"].keys()

    # Busca os dados dos jogadores
        match_players = self.player_gateway.get_players(players_ids)

    # Copia o partido escolhido no lobby para o jogador da partida
        for match_player in match_players:
            player_id = match_player["player_id"]

            room_player = room_dict["players"].get(player_id)

            if room_player is None:
             raise ValueError(
                    f"Jogador {player_id} não encontrado na sala"
                )

            party_id = room_player.get("party_id")

            if party_id is None:
                raise ValueError(
                    f"Jogador {player_id} não escolheu um partido"
                )

            match_player["party_id"] = party_id

        match_dict = Match.create_dict(
        match_id=match_id,
        territories=match_territories,
        room_code=room_dict["room_code"],
        players=match_players,
        status="running",
        current_turn_player_id=next(iter(room_dict["players"])),
        round=1,
        missions=[],
    )

        return match_dict
    def advance_turn(self,match_dict: dict):
            players = match_dict["players"]
            current_player_id = match_dict["current_turn_player_id"]
    
            current_index = 0
    
            for index, player in enumerate(players):
                if player["player_id"] == current_player_id:
                    current_index = index
                    break
    
            next_index = (current_index + 1) % len(players)
    
            if next_index == 0:
                match_dict["round"] += 1
    
            match_dict["current_turn_player_id"] = players[next_index]["player_id"]
    def change_key_value(self,match_dict,key,newValue):
        match_dict[key]=newValue
        return match_dict
    def clean_key_value(self,key,match_dict):
        match_dict.pop(key,None)
        return match_dict
    def finish_match(self,match,player_id,action_result):
        match["status"] = "finished"
        match["winner_id"] = player_id
        match["last_action_result"] = action_result
        return match
    def switch_question_list(self,match_dict,question,pop_name_list_questions):
        if pop_name_list_questions == "questions_1":
            put_name_list_questions="questions_2"
        else:
            pop_name_list_questions = "questions_2"
            put_name_list_questions="questions_1"
        pop_list : list[dict]=match_dict[pop_name_list_questions]
        put_list : list [dict]=match_dict[put_name_list_questions]
        pop_list.remove(question)
        put_list.append(question)
        match_dict["activate_questions_list"] = pop_name_list_questions
        self.update_match(match_dict)
    def return_to_room(self,match_dict):
        pass