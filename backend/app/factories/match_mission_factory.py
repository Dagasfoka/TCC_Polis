import random

from backend.app.models.match_mission import MatchMission
from backend.app.repositories.match_mission_repo import (
    get_match_mission_by_owner_id,
    update_match_mission,
)
from backend.app.services.factories.match_verify_factory import (
    is_alive,
    verify_region,
    verify_state,
)


def start_verify_match_mission(match_id, player_id):
    match_mission = get_match_mission_by_owner_id(match_id, player_id)

    if match_mission is None:
        raise ValueError("Missão do jogador não encontrada.")

    if match_mission["type"] == "destruction":
        target_id = match_mission["content"]["destruction"]

        if not is_alive(match_id, target_id):
            match_mission["type"] = "state"
            update_match_mission(match_id, match_mission)
            return True

    return False


def final_verify_match_mission(match_id, player_id):
    match_mission = get_match_mission_by_owner_id(match_id, player_id)

    if match_mission is None:
        raise ValueError("Missão do jogador não encontrada.")

    match match_mission["type"]:
        case "region":
            for region_content in match_mission["content"]["region"]:
                if not verify_region(
                    region_content["region"],
                    region_content["quantity"],
                    match_id,
                    match_mission["owner_id"],
                ):
                    return False

            return True

        case "state":
            return verify_state(
                match_mission["content"]["state"],
                match_mission["owner_id"],
                match_id,
            )

        case "destruction":
            return not is_alive(
                match_id,
                match_mission["content"]["destruction"],
            )

        case _:
            raise ValueError(f"Tipo de missão inválido: {match_mission['type']}")


def choose_missions(missions, quantity_players):
    if len(missions) < quantity_players:
        raise ValueError("Não há missões suficientes para todos os jogadores.")

    return random.sample(missions, quantity_players)


def distribute_match_missions(match_id, players, chosen_missions):
    if len(players) != len(chosen_missions):
        raise ValueError("A quantidade de players precisa ser igual à quantidade de missões.")

    match_missions = []

    for player, mission in zip(players, chosen_missions):
        content = mission.content.copy()

        if mission.type == "destruction":
            content["destruction"] = choose_destruction_target(
                players=players,
                owner_id=player["player_id"],
            )

        match_mission = MatchMission(
            match_id=match_id,
            mission_id=mission.mission_id,
            type=mission.type,
            content=content,
            owner_id=player["player_id"],
        )

        match_missions.append(match_mission.to_dict())

    return match_missions


def choose_destruction_target(players, owner_id):
    possible_targets = [
        player["player_id"]
        for player in players
        if player["player_id"] != owner_id
    ]

    if not possible_targets:
        raise ValueError("Não há alvo possível para missão de destruição.")

    return random.choice(possible_targets)