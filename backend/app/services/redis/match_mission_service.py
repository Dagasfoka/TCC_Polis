from backend.app.factories.match_mission_factory import MatchMissionFactory

match_mission_factory=MatchMissionFactory()
def start_round_verify(match_id,player_id):
    return match_mission_factory.start_verify_match_mission(match_id,player_id)
def final_round_verify(match_id,player_id):
    return match_mission_factory.final_verify_match_mission(match_id,player_id)
    