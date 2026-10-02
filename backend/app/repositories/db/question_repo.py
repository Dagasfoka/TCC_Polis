from sqlalchemy import inspect, select
from sqlalchemy.orm import Session

from backend.app.models.db.question import Question


class QuestionRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_all_questions(self):
        return list(self.db.scalars(select(Question)).all())

    def to_dict(self, question: Question) -> dict:
        return {
            column.key: getattr(question, column.key)
            for column in inspect(Question).column_attrs
        }

    def get_all_questions_dict(self) -> list[dict]:
        return [
            self.to_dict(question)
            for question in self.get_all_questions()
        ]