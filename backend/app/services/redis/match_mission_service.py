from backend.app.factories.redis.match_mission_factory import (
    final_verify_match_mission,
    start_verify_match_mission,
)
from backend.app.services.redis.match_service import (
    get_match_mission_by_owner_service,
)
from backend.app.validators.match_mission_validator import (
    verify_match_mission_exist,
)


def start_round_verify(match_id,player_id):
    verify_match_mission_exist()
    get_match_mission_by_owner_service(match_id,player_id)
    return start_verify_match_mission(match_id,player_id)
def final_round_verify(match_id,player_id):
    return final_verify_match_mission(match_id,player_id)
    