from sqlalchemy import Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Action(Base):
    __tablename__ = "actions"

    action_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    action_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    alignment: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    responses: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    def to_dict(self) -> dict:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "alignment": self.alignment,
            "title": self.title,
            "description": self.description,
            "risk_level": self.risk_level,
            "responses": self.responses,
        }