from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.db.question import Question


class QuestionRepo:

    def __init__(self, db: Session):
        self.db = db

    def get_all_questions(self):
        return self.db.scalars(
            select(Question)
        ).all()
