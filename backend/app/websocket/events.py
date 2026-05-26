from backend.app.repositories.match_mission_repo import get_match_mission_by_owner_id
from backend.app.services.action_service import get_attack_options


def build_personal_match_state(match_dict: dict, player_id: str):
    match_id = match_dict["match_id"]
    your_mission = get_match_mission_by_owner_id(match_id, player_id)

    return {
        "type": "match_state",
        "payload": {
            "match_id": match_dict["match_id"],
            "territories": match_dict["territories"],
            "room_code": match_dict["room_code"],
            "players": match_dict["players"],
            "status": match_dict["status"],
            "current_turn_player_id": match_dict["current_turn_player_id"],
            "round": match_dict["round"],
            "winner_id": match_dict.get("winner_id"),
            "last_action_result": match_dict.get("last_action_result"),
            "available_attack_options": get_attack_options(),
            "your_player_id": player_id,
            "your_mission": your_mission,
        },
    }


def build_error(message: str):
    return {
        "type": "error",
        "payload": {
            "message": message,
        },
    }