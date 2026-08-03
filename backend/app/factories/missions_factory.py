import random
def distribute_questions(match_state_dict,questions):
    for player in match_state_dict["players"]:
        player_questions = [question.copy() for question in questions]
        random.shuffle(player_questions)
        player["questions"] = player_questions
    return match_state_dict