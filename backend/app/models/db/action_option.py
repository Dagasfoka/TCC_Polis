from dataclasses import dataclass


@dataclass
class ActionOption:
    option_id: str
    action_type: str
    title: str
    description: str
    cost_money: int
    success_chance: int
    influence_generated: int
    risk_level: str

    def to_dict(self):
        return {
            "option_id": self.option_id,
            "action_type": self.action_type,
            "title": self.title,
            "description": self.description,
            "cost_money": self.cost_money,
            "success_chance": self.success_chance,
            "influence_generated": self.influence_generated,
            "risk_level": self.risk_level,
        }