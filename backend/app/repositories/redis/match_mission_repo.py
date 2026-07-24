from backend.app.repositories.redis.match_repo import get_match_state, save_match_state


def get_all_match_missions(match_id):
    match_dict = get_match_state(match_id)

    if match_dict is None:
        raise ValueError("Partida não encontrada.")

    return match_dict.get("missions", [])


def get_match_mission_by_id(match_id, mission_id):
    for mission in get_all_match_missions(match_id):
        if mission["mission_id"] == mission_id:
            return mission

    return None


def get_match_mission_by_owner_id(match_id, owner_id):
    for mission in get_all_match_missions(match_id):
        if mission["owner_id"] == owner_id:
            return mission

    return None


def create_match_mission(match_id, match_mission_dict):
    match_dict = get_match_state(match_id)

    if match_dict is None:
        raise ValueError("Partida não encontrada.")

    missions = match_dict.setdefault("missions", [])

    owner_id = match_mission_dict["owner_id"]

    for mission in missions:
        if mission["owner_id"] == owner_id:
            raise ValueError("Esse jogador já possui uma missão nessa partida.")

    missions.append(match_mission_dict)

    save_match_state(match_dict)

    return match_mission_dict


def save_match_missions(match_id, match_missions):
    match_dict = get_match_state(match_id)

    if match_dict is None:
        raise ValueError("Partida não encontrada.")

    match_dict["missions"] = match_missions

    save_match_state(match_dict)

    return match_missions

def update_match_mission(match_id, updated_match_mission):
    match_dict = get_match_state(match_id)

    if match_dict is None:
        raise ValueError("Partida não encontrada.")

    missions = match_dict.get("missions", [])

    for index, mission in enumerate(missions):
        if mission["owner_id"] == updated_match_mission["owner_id"]:
            missions[index] = updated_match_mission
            save_match_state(match_dict)
            return updated_match_mission

    raise ValueError("Missão do jogador não encontrada.")