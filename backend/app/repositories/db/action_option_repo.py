from backend.app.models.db.action_option import ActionOption

ATTACK_OPTIONS = [
    ActionOption(
        option_id="safe_company",
        action_type="attack",
        title="Contratar empresa consolidada",
        description=(
            "Você contrata uma empresa grande e reconhecida. "
            "A ação custa mais, mas tem menor risco e gera influência moderada."
        ),
        cost_money=80,
        success_chance=80,
        influence_generated=4,
        risk_level="baixo",
    ),
    ActionOption(
        option_id="small_company",
        action_type="attack",
        title="Contratar empresa menor",
        description=(
            "Você contrata uma empresa menor e mais barata. "
            "A ação tem maior risco, mas pode gerar muito mais influência."
        ),
        cost_money=40,
        success_chance=45,
        influence_generated=8,
        risk_level="alto",
    ),
]


def list_options_by_action(action_type: str):
    return [
        option.to_dict()
        for option in ATTACK_OPTIONS
        if option.action_type == action_type
    ]


def get_option_by_id(option_id: str):
    for option in ATTACK_OPTIONS:
        if option.option_id == option_id:
            return option.to_dict()

    return None