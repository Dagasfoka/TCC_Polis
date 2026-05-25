#Questions do game.
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    question_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject: Mapped[str] = mapped_column(String(30), nullable=False)
    board: Mapped[str] = mapped_column(String(10),nullable=False)
    answer: Mapped[bool] = mapped_column (Boolean,nullable=False )
    def __repr__(self) -> str:
        return (
            f"Question(id={self.question_id!r}, "
            f"subject={self.subject!r}, "
            f"board={self.board!r}, "
            f"answer={self.answer!r})"
        )
    def to_dict(self):
        return {
            'question_id':self.question_id,
            'subject':self.subject,
            'board': self.board,
            'answer': self.answer,
        }