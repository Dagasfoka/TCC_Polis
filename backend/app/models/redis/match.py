class Match:
    def __init__(
        self,
        match_id: int,
        territories: list[dict],
        room_code,
        players: list[dict],
        status: str,
        current_turn_player_id: str,
        round,
        activate_questions_list : str | None = None,
        questions_1 : list[dict] | None = None,
        questions_2 : list[dict] | None = None,
        missions: list[dict] | None = None,
        pending_action : dict | None = None,
        winner_id : str | None = None,
    ):
        self.match_id = match_id
        self.territories = territories
        self.room_code = room_code
        self.players = players
        self.status = status
        self.current_turn_player_id = current_turn_player_id
        self.round = round
        self.missions = missions or []
        self.pending_action= pending_action,
        self.winner_id=winner_id
        self.questions_1=questions_1 or []
        self.questions_2=questions_2 or []
        self.activate_questions_list = activate_questions_list

    def to_dict(self):
        return {
            "match_id": self.match_id,
            "territories": self.territories,
            "room_code": self.room_code,
            "players": self.players,
            "status": self.status,
            "current_turn_player_id": self.current_turn_player_id,
            "round": self.round,
            "missions": self.missions,
            "pending_action" :self.pending_action ,
            "winner_id" : self.winner_id,
            "activate_questions_list": self.activate_questions_list,
            "questions_1" : self.questions_1,
            "questions_2" : self.questions_2,
                }

    @classmethod
    def create_dict(
        cls,
        match_id: int,
        territories: list[dict],
        room_code,
        players: list[dict],
        status: str,
        current_turn_player_id: str,
        round,
        activate_questions_list: str | None=None,
        questions_1: list[dict] | None=None,
        questions_2: list[dict] | None=None,
        missions: list[dict] | None = None,
        pending_action : dict | None = None,
        winner_id : str | None = None,
    ):
        return cls(
            match_id,
            territories,
            room_code,
            players,
            status,
            current_turn_player_id,
            round,
            activate_questions_list,
            questions_1,
            questions_2,
            missions,
            pending_action,
            winner_id,
        ).to_dict()