# Jogador dentro de uma partida.
class Player:
    def __init__(
        self,
        player_id: str,
        match_id: int,
        party_id: int,
        player_token: str,
        username: str, 
        questions: dict | None =None,
    ):
        self.player_id = player_id
        self.match_id = match_id
        self.party_id = party_id
        self.questions = questions
        self.player_token = player_token
        self.username = username

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "match_id": self.match_id,
            "party_id": self.party_id,
            "username": self.username,
            'questions': self.questions
        }
 