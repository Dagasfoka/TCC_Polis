from backend.app.repositories.db.question_repo import  QuestionRepo
class QuestionGateways:
    def __init__(self) -> None:
        self.question_repo=QuestionRepo()
    def get_all_questions(self):
        return self.question_repo.get_all_questions()