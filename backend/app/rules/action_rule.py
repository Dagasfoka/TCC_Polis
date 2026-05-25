QUESTION_CORRECT_BONUS = 10
QUESTION_WRONG_PENALTY = 10

MIN_SUCCESS_CHANCE = 5
MAX_SUCCESS_CHANCE = 95

def adjust_success_chance_by_answer(
    base_success_chance: int,
    question_was_correct: bool,
) -> int:
    if question_was_correct:
        adjusted_success_chance = base_success_chance + QUESTION_CORRECT_BONUS
    else:
        adjusted_success_chance = base_success_chance - QUESTION_WRONG_PENALTY

    return clamp_success_chance(adjusted_success_chance)

#_____________________________AUX_____________________________________________

def clamp_success_chance(success_chance: int) -> int:
    return max(MIN_SUCCESS_CHANCE, min(MAX_SUCCESS_CHANCE, success_chance))
