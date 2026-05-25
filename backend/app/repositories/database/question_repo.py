from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.database.question_model import Question

#ERRO {
QUESTIONS_OPTIONS = [
    {
        "question_id":1,
        "subject":"Philosofy",
        "description": "O conceito de contrato social está associado a Rousseau?",
        "answer":True,
    },
    {
        "question_id":2,
        "subject":"Geography",
        "description": "O Brasil está localizado no hemisfério norte?",
        "answer":False,
    },
    {
        "question_id":3,
        "subject":"History",
        "description": "A Revolução Francesa ocorreu no século XVIII?",
        "answer":True,
    },
    {
        "question_id":4,
        "subject":"Sociology",
        "description":"A socialização ocorre apenas na infância?",
        "answer":False,
    },
    {
        "question_id":5,
        "subject":"Philosofy",
        "description":"Platão foi discípulo de Sócrates?",
        "answer":True,
    },
    {
        "question_id":6,
        "subject":"Geography",
        "description":"A linha do Equador divide a Terra em dois hemisférios?",
        "answer":True,
    },
    {
        "question_id":7,
        "subject":"History",
        "description":"O Brasil foi colonizado pela Espanha?",
        "answer":False,
    },
    {
        "question_id":8,
        "subject":"Sociology",
        "description":"Cultura é tudo aquilo que é aprendido socialmente?",   
        "answer":True,
    },
]
# } ERRO
# -> criar script pra criação das QuestionOptions
#DIFF : EASY

### ERRO Mudar todas as variáveis QUESTIONS_OPTIONS 
#DIFF : EASY
def list_questions():
    return [
        question
        for question in QUESTIONS_OPTIONS 
    ]


def get_question_by_id(question_id: str):
    for question in QUESTIONS_OPTIONS:
        if question.question_id == question_id:
            return question
    return None


def get_all_questions_dict(db: Session) -> list[dict]:
    return [q.to_dict() for q in db.scalars(select(Question)).all()]

def get_all_questions(db: Session) -> list[Question]:
    return list (db.scalars(select(Question)).all())


def get_question_by_id(db: Session, question_id: int) -> dict | None:
    return db.get(Question, question_id).to_dict()