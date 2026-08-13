# backend/app/scripts/seed_questions.py

from sqlalchemy import delete

from backend.app.db.base import Base
from backend.app.db.database import SessionLocal, engine
from backend.app.models.db.question import Question

QUESTIONS = [
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

def seed_questions():
    Base.metadata.create_all(bind=engine)

    with SessionLocal.begin() as db:
        db.execute(delete(Question))

        questions = [
            Question(**question_data)
            for question_data in QUESTIONS
        ]

        db.add_all(questions)
