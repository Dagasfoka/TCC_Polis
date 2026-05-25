def verify_questions_exist(questions):
    if not questions:
        raise ValueError("Esse jogador não possui mais perguntas disponíveis")