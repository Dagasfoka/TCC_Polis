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
        missions: list[dict] | None = None,
    ):
        self.match_id = match_id
        self.territories = territories
        self.room_code = room_code
        self.players = players
        self.status = status
        self.current_turn_player_id = current_turn_player_id
        self.round = round
        self.missions = missions or []

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
        missions: list[dict] | None = None,
    ):
        return cls(
            match_id,
            territories,
            room_code,
            players,
            status,
            current_turn_player_id,
            round,
            missions,
        ).to_dict()