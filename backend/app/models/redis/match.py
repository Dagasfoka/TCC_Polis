class Match:
    def __init__(
        self,
        match_id: int,
        territories: list[dict],
        room_code: str,
        players: list[dict],
        status: str,
        current_turn_player_id: str,
        round: int,
        activate_questions_list: str | None = None,
        questions_1: list[dict] | None = None,
        questions_2: list[dict] | None = None,
        missions: list[dict] | None = None,
        pending_action: dict | None = None,
        winner_id: str | None = None,
        attack_actions_1: list[dict] | None = None,
        defense_actions_1: list[dict] | None = None,
        attack_actions_2: list[dict] | None = None,
        defense_actions_2: list[dict] | None = None,
        activate_attack_actions_list: str | None = None,
        activate_defense_actions_list: str | None = None,
        round_attack_actions: list[dict] | None = None,
        round_defense_actions: list[dict] | None = None,
        phase: str = "initial_distribution",
        last_action_result: dict | None = None,
    ):
        self.match_id = match_id
        self.territories = territories
        self.room_code = room_code
        self.players = players
        self.status = status
        self.current_turn_player_id = current_turn_player_id
        self.round = round
        self.phase = phase

        self.missions = missions if missions is not None else []
        self.pending_action = pending_action
        self.winner_id = winner_id
        self.last_action_result = last_action_result

        self.activate_questions_list = activate_questions_list
        self.questions_1 = questions_1 if questions_1 is not None else []
        self.questions_2 = questions_2 if questions_2 is not None else []

        self.attack_actions_1 = (
            attack_actions_1 if attack_actions_1 is not None else []
        )
        self.defense_actions_1 = (
            defense_actions_1 if defense_actions_1 is not None else []
        )
        self.attack_actions_2 = (
            attack_actions_2 if attack_actions_2 is not None else []
        )
        self.defense_actions_2 = (
            defense_actions_2 if defense_actions_2 is not None else []
        )

        self.activate_attack_actions_list = activate_attack_actions_list
        self.activate_defense_actions_list = activate_defense_actions_list

        self.round_attack_actions = (
            round_attack_actions if round_attack_actions is not None else []
        )
        self.round_defense_actions = (
            round_defense_actions if round_defense_actions is not None else []
        )

    def to_dict(self) -> dict:
        return {
            "match_id": self.match_id,
            "territories": self.territories,
            "room_code": self.room_code,
            "players": self.players,
            "status": self.status,
            "current_turn_player_id": self.current_turn_player_id,
            "round": self.round,
            "phase": self.phase,
            "missions": self.missions,
            "pending_action": self.pending_action,
            "winner_id": self.winner_id,
            "last_action_result": self.last_action_result,
            "activate_questions_list": self.activate_questions_list,
            "questions_1": self.questions_1,
            "questions_2": self.questions_2,
            "attack_actions_1": self.attack_actions_1,
            "defense_actions_1": self.defense_actions_1,
            "attack_actions_2": self.attack_actions_2,
            "defense_actions_2": self.defense_actions_2,
            "activate_attack_actions_list": self.activate_attack_actions_list,
            "activate_defense_actions_list": self.activate_defense_actions_list,
            "round_attack_actions": self.round_attack_actions,
            "round_defense_actions": self.round_defense_actions,
        }

    @classmethod
    def create_dict(
        cls,
        match_id: int,
        territories: list[dict],
        room_code: str,
        players: list[dict],
        status: str,
        current_turn_player_id: str,
        round: int,
        activate_questions_list: str | None = None,
        questions_1: list[dict] | None = None,
        questions_2: list[dict] | None = None,
        missions: list[dict] | None = None,
        pending_action: dict | None = None,
        winner_id: str | None = None,
        attack_actions_1: list[dict] | None = None,
        defense_actions_1: list[dict] | None = None,
        attack_actions_2: list[dict] | None = None,
        defense_actions_2: list[dict] | None = None,
        activate_attack_actions_list: str | None = None,
        activate_defense_actions_list: str | None = None,
        round_attack_actions: list[dict] | None = None,
        round_defense_actions: list[dict] | None = None,
        phase: str = "initial_distribution",
        last_action_result: dict | None = None,
    ) -> dict:
        return cls(
            match_id=match_id,
            territories=territories,
            room_code=room_code,
            players=players,
            status=status,
            current_turn_player_id=current_turn_player_id,
            round=round,
            activate_questions_list=activate_questions_list,
            questions_1=questions_1,
            questions_2=questions_2,
            missions=missions,
            pending_action=pending_action,
            winner_id=winner_id,
            attack_actions_1=attack_actions_1,
            defense_actions_1=defense_actions_1,
            attack_actions_2=attack_actions_2,
            defense_actions_2=defense_actions_2,
            activate_attack_actions_list=activate_attack_actions_list,
            activate_defense_actions_list=activate_defense_actions_list,
            round_attack_actions=round_attack_actions,
            round_defense_actions=round_defense_actions,
            phase=phase,
            last_action_result=last_action_result,
        ).to_dict()