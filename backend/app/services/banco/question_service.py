from backend.app.validators.question_validator import verify_questions_exist


def get_next_question_for_player(player: dict):
    questions : dict = player.get("questions", [])

    verify_questions_exist(questions)

    question = questions.pop(0)

    return question
