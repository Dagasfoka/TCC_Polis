from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.database.action_option_model import Action_Option, ActionOption
# ERRO{
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
# }ERRO
# -> criar script pra criação das ActionOption
#DIFF : EASY

### ERRO Mudar todas as variáveis ATTACK_OPTIONS 
#DIFF : EASY
def list_options_by_action(action_type: str):
    return [
        option.to_dict()
        for option in ATTACK_OPTIONS
        if option.action_type == action_type
    ]


def get_option_by_id_repo(option_id: str):
    for option in ATTACK_OPTIONS:
        if option.option_id == option_id:
            return option.to_dict()

    return None

def get_all_action_options_dict(db: Session) -> list[dict]:
    return [action_option.to_dict() for action_option in db.scalars(select(Action_Option)).all()]

def get_all_action_options(db: Session) -> list[Action_Option]:
    return list (db.scalars(select(Action_Option)).all())


def get_action_option_by_id(db: Session, Action_Option_id: int) -> dict | None:
    return db.get(Action_Option, Action_Option_id).to_dict()