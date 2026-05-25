
from backend.app.repositories.database.action_option_repo import (
    get_option_by_id_repo,
    list_options_by_action,
)


def get_option_by_id(option_id):
    return get_option_by_id_repo(option_id)
def get_all_options_by_type(type):
    return list_options_by_action(type)