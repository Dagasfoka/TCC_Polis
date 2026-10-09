from backend.app.repositories.redis.match_repo import MatchRepo

class MatchValidator:
    def __init__(self) -> None:
        self.match_repository=MatchRepo()
#_________________________________________________ Simples
    def match_exist(self,match_dict):
        if match_dict is None:
           raise Exception("Partida não existe") 
        return match_dict 
    def territory_exist(self,territory):
        if territory is None:
           raise Exception("Território não existe") 
        return territory 
    def verify_match_status(self,match_dict,status):
        if match_dict["status"] != status:
            raise ValueError("Partida não está em andamento")
        return match_dict
    def verify_current_turn_player_id(self,match_dict,player_id):
        if match_dict["current_turn_player_id"] != player_id:
            raise ValueError("Não é o turno desse jogador")
        return match_dict
    def round_exist(self,round):
        if round is None:
           raise Exception("Round não encontrado") 
        return round
    def questions_exist(self,questions):
        if questions is None:
           raise Exception("Questões não encontradas") 
        return questions
    def verify_player_match_influence_is_not_below_zero(self,match_influence):
        if match_influence<0:
            raise Exception("Influência geral do player menor que zero") 
        return match_influence
#_________________________________________________ AUX
    def is_alive(self,match_id, target_id):
        match_dict = self.match_repository.get_match(match_id)
        match_dict=self.match_exist(match_dict)
        territories = match_dict["territories"]

        for territory in territories:
            if territory["owner_id"] == target_id:
                return True

        return False


    def verify_state(self,states_id: list[str], owner_id: str, match_id: str):
        match_dict = self.match_repository.get_match(match_id)

        for state_id in states_id:
            state=self.match_repository.get_territory_by_id(match_dict, state_id)
            state=self.territory_exist(state)
            if state["owner_id"] != owner_id:
                return False

        return True


    def verify_region(self,region: str, quantity: int, match_id, owner_id: str) -> bool:
        match_dict = self.match_repository.get_match(match_id)

        territories = self.match_repository.get_territory_by_region(match_dict, region)

        owned_territories = [
            territory for territory in territories
            if territory["owner_id"] == owner_id
        ]

        return len(owned_territories) >= quantity
    def verify_match_finish(self,match_dict: dict) -> bool:
        if match_dict["status"]=="finished":
            return True
        return False
    def verify_distribute_match_influence(self,match_influence):
        if match_influence >0:
            return True
        return False
    """
    def aux_writer(self,match_id,player_id): #To fazendo esse so pra poder digitar e pensar sem afetar algo que alguem possivelmente ta mexendo
        match=match_id #get match
        player= player_id #find match player
        match_influence=player['match_influence']
        match_influence=self.verify_player_match_influence_is_not_below_zero(match_influence,player)
        if self.verify_distribute_match_influence(match_influence):
            # do something
        return "ainda nao sei"
    """