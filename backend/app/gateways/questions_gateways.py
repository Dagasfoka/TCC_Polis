from sqlalchemy.orm import Session

from backend.app.repositories.db.question_repo import  QuestionRepo

class QuestionGateways:
    def __init__(self, db: Session) -> None:
        self.question_repo=QuestionRepo(db)
    def get_all_questions(self):
        return self.question_repo.get_all_questions()
