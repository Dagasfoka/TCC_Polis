class PendingAction:
    def __init__(
        self,
        player_id: str,
        target_territory_id: str,
        option_id: int,
        question_id: int,
        correct_answer: bool,
        action_type : str
    ):
        self.player_id = player_id
        self.target_territory_id = target_territory_id
        self.option_id = option_id
        self.question_id = question_id
        self.correct_answer = correct_answer
        self.action_type = action_type

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "target_territory_id": self.target_territory_id,
            "option_id": self.option_id,
            "question_id": self.question_id,
            "correct_answer": self.correct_answer,
            "action_type": self.action_type
        }

    @classmethod
    def create_dict(
        cls,
        player_id: str,
        target_territory_id: str,
        option_id: int,
        question_id: int,
        correct_answer: bool,
        action_type:str,
    ):
        return cls(
            player_id,
            target_territory_id,
            option_id,
            question_id,
            correct_answer,
            action_type
        ).to_dict()