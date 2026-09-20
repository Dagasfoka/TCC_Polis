from backend.app.gateways.questions_gateways import QuestionGateways
import random 
class MatchQuestionFactory:
    def __init__(self,db) -> None:
        self.questions_gateway = QuestionGateways(db=db)
    def distribute_questions(self,players):
        questions=self.questions_gateway.get_all_questions()
        
        for player in players:
            player_questions = [question.to_dict() for question in questions]
            random.shuffle(player_questions)
            player["questions"] = player_questions
        return players