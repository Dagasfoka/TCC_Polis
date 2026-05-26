from backend.app.repositories.match_repo import (
    get_match_state,
    get_territory_by_id,
    get_territory_by_region,
)


def is_alive(match_id, target_id):
    match_dict = get_match_state(match_id)
    territories = match_dict["territories"]

    for territory in territories:
        if territory["owner_id"] == target_id:
            return True

    return False


def verify_state(states_id: list[str], owner_id: str, match_id: str):
    match_dict = get_match_state(match_id)

    for state_id in states_id:
        if get_territory_by_id(match_dict, state_id)["owner_id"] != owner_id:
            return False

    return True


def verify_region(region: str, quantity: int, match_id, owner_id: str) -> bool:
    match_dict = get_match_state(match_id)

    territories = get_territory_by_region(match_dict, region)

    owned_territories = [
        territory for territory in territories
        if territory["owner_id"] == owner_id
    ]

    return len(owned_territories) >= quantity