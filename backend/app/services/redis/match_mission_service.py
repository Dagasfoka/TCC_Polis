from backend.app.factories.redis.match_mission_factory import (
    final_verify_match_mission,
    start_verify_match_mission,
)


def start_round_verify(match_id,player_id):
    return start_verify_match_mission(match_id,player_id)
def final_round_verify(match_id,player_id):
    return final_verify_match_mission(match_id,player_id)
    