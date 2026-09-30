from backend.app.repositories.redis.player_repo import  PlayerRepo
class PlayerGateway:
    def __init__(self) -> None:
        self.player_repository=PlayerRepo()
    def get_players(self, player_ids):
        players = []
        for player_id in player_ids:
            player = self.get_player(player_id)
            players.append(player)

        return players
    def get_player(self,player_id):
        return self.player_repository.get_player(player_id)
    def get_next_question_for_player(self, player: dict):
        questions = player.get("questions", [])
        if not questions:
            raise ValueError("Esse jogador não possui mais perguntas disponíveis")

        question = questions.pop(0)

        return question