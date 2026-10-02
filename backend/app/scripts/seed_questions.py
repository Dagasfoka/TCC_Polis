# Perguntas convertidas do arquivo fornecido; bancas e gabaritos não verificados.
from sqlalchemy import delete

from backend.app.db.base import Base
from backend.app.db.database import SessionLocal, engine
from backend.app.models.db.question import Question

QUESTIONS = [
    {
        "subject": "Philosophy",
        "description": "No dia 1º de abril de 1964 aconteceu o golpe militar. O regime político nascido do golpe cometeu diversos crimes contra os direitos humanos. Sobre os Direitos Humanos, é correto afirmar que se fundamentam filosoficamente na consciência social de uma época, segundo a opinião da maioria das pessoas?",
        "exam_board": "UECE-CEV 2024 - Adaptado",
        "options": {
            "A": "Verdadeiro",
            "B": "Falso"
        },
        "answer": "B",
        "difficulty": "easy",
        "explanation": "Na verdade se fundamentam filosoficamente no direito natural e são reconhecidos pela razão, independente das opiniões ou das leis. Mesmo que o Estado viole direitos, eles continuam existindo, dessa forma, permite criticar governos injustos com base em princípios além da lei."
    },
    {
        "subject": "Philosophy",
        "description": "Sobre os conceitos de ética, moral e cidadania, assinale a alternativa correta:",
        "exam_board": "CETREDE - Prefeitura de Maracanaú - 2026 - Adaptado",
        "options": {
            "A": "A ética busca princípios universais de convivência, enquanto a moral varia conforme a cultura e o contexto histórico.",
            "B": "A cidadania está restrita apenas à participação eleitoral em sistemas democráticos."
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "A ética reflete princípios gerais sobre o agir humano; a moral corresponde aos costumes e valores específicos de cada sociedade."
    },
]

def seed_questions():
    Base.metadata.create_all(bind=engine)

    with SessionLocal.begin() as db:
        db.execute(delete(Question))
        db.add_all([Question(**data) for data in QUESTIONS])

    print(f"{len(QUESTIONS)} questões cadastradas.")


if __name__ == "__main__":
    seed_questions()
