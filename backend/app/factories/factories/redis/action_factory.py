

def build_action_response_before_question(type,player_id,target,target_territory_id,option,question):
    {
        "type": type,
        "player_id": player_id,
        "target_territory_id": target_territory_id,
        "territory_name": target.get("name"),
        "option_id": option.get("option_id"),
        "title": option.get("title"),
        "description": option.get("description"),
        "risk_level": option.get("risk_level"),
        "cost_money": option.get("cost_money"),
        "success_chance": option.get("success_chance"),
        "question": {
        "question_id": question.get("question_id"),
        "subject": question.get("subject"),
        "description": question.get("description"),
                },
    },
#ERRO - passar mt coisa do action service pra ca
#o qq isso ta fzndw