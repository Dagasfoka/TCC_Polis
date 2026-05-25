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
        

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Action_Option(Base):
    __tablename__ = "action_options"

    option_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_type: Mapped[str] = mapped_column(String(30), nullable=False)
    title: Mapped[str] = mapped_column(String(50),nullable=False)
    description: Mapped[str] = mapped_column (String(150),nullable=False )
    cost_money: Mapped[int] = mapped_column (Integer, nullable=False)
    sucess_chance: Mapped[int] = mapped_column (Integer, nullable=False)
    influence_generated: Mapped[int] = mapped_column (Integer, nullable=False)
    risk_level: Mapped[str] = mapped_column (String, nullable=False)
    def __repr__(self) -> str:
        return (
        f"ActionOption("
        f"option_id={self.option_id!r}, "
        f"action_type={self.action_type!r}, "
        f"title={self.title!r}, "
        f"cost_money={self.cost_money!r}, "
        f"success_chance={self.success_chance!r}, "
        f"influence_generated={self.influence_generated!r}, "
        f"risk_level={self.risk_level!r}"
        f")"
        )
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