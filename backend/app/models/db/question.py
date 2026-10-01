# backend/app/models/db/question.py

from sqlalchemy import Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    question_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    subject: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    exam_board: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    options: Mapped[dict[str, str]] = mapped_column(
        JSON,
        nullable=False,
    )

    answer: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    explanation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    def to_dict(self) -> dict:
        return {
            "question_id": self.question_id,
            "subject": self.subject,
            "description": self.description,
            "exam_board": self.exam_board,
            "options": self.options,
            "answer": self.answer,
            "difficulty": self.difficulty,
            "explanation": self.explanation,
        }