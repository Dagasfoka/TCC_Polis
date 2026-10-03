from dataclasses import dataclass

@dataclass
class MatchAction:
    action_id: int

    action_type: str

    alignment: str

    title: str

    description: str

    risk_level: str

    responses: dict[str, str]

    cost: int
    influence: int
    money: int
    corruption: int = 0
    positive_critical: int | None = None
    negative_critical: int | None = None
    success_chance: int | None = None

    def to_dict(self):
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "alignment": self.alignment,
            "title": self.title,
            "description": self.description,
            "risk_level": self.risk_level,
            "responses": self.responses,
            "positive_critical": self.positive_critical,
            "negative_critical": self.negative_critical,
            "success_chance": self.success_chance,
            "cost": self.cost,
            "influence": self.influence,
            "money": self.money,
            "corruption": self.corruption,
        }