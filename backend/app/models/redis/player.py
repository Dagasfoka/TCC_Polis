# Jogador dentro de uma partida.
class Player:
    def __init__(
        self,
        player_id: str,
        match_id: int | None,
        party_id: int | None,
        player_token: str,
        username: str,
        questions: dict | None = None,
        match_influence: int | None = 0,
        match_money: int | None = 0,
        match_corruption: int | None = 0,
    ):
        self.player_id = player_id
        self.match_id = match_id
        self.party_id = party_id
        self.player_token = player_token
        self.username = username
        self.questions = questions
        self.match_influence = match_influence
        self.match_money = match_money
        self.match_corruption = match_corruption

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "match_id": self.match_id,
            "party_id": self.party_id,
            "player_token": self.player_token,
            "username": self.username,
            "questions": self.questions,
            "match_influence": self.match_influence,
            "match_money": self.match_money,
            "match_corruption": self.match_corruption,
        }

    @classmethod
    def create_dict(
        cls,
        player_id: str,
        match_id: int | None,
        party_id: int | None,
        player_token: str,
        username: str,
        questions: dict | None = None,
        match_influence: int | None = 0,
        match_money: int | None = 0,
        match_corruption: int | None = 0,
    ):
        return cls(
            player_id,
            match_id,
            party_id,
            player_token,
            username,
            questions,
            match_influence,
            match_money,
            match_corruption,
        ).to_dict()