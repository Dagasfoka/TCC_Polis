# backend/app/models/db/question.py

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    question_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    subject: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    answer: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    def to_dict(self) -> dict:
        return {
            "question_id": self.question_id,
            "subject": self.subject,
            "description": self.description,
            "answer": self.answer
        }
