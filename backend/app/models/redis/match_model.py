# Status geral da partida.
from backend.app.models.redis.match_territory_model import MatchTerritory
from backend.app.models.redis.player_model import Player


class Match:
    def __init__(
        self,
        match_id: int,
        territories: list[MatchTerritory],
        room_code,
        players: list[Player],
        status: str,
        current_turn_player_id: str,
        round,
        missions: list[dict] | None = None,
        pending_action_question: dict | None=None,
    ):
        self.match_id = match_id
        self.territories = territories
        self.room_code = room_code
        self.players = players
        self.status = status
        self.current_turn_player_id = current_turn_player_id
        self.round = round
        self.missions = missions or []
        self.pending_action_question=pending_action_question

    def to_dict(self):
        return {
            "match_id": self.match_id,
            "territories": [t.to_dict() for t in self.territories],
            "room_code": self.room_code,
            "players": [p for p in self.players],
            "status": self.status,
            "current_turn_player_id": self.current_turn_player_id,
            "round": self.round,
            "missions": self.missions,
            'pending_action_question': self.pending_action_question,
        }