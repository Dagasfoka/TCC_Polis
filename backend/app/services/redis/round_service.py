from backend.app.factories.match_action_factory import MatchActionFactory
from backend.app.validators.match_validators import MatchValidator
from backend.app.gateways.match_gateways import MatchGateway
from backend.app.validators.player_validators import PlayerValidator
from backend.app.validators.match_distribute_validators import (
    MatchDistributeValidator,
)
from backend.app.factories.match_factory import MatchFactory

import random


match_factory = MatchFactory()
match_validator = MatchValidator()
match_gateway = MatchGateway()
player_validator = PlayerValidator()
match_action_factory = MatchActionFactory()
match_distribute_validator = MatchDistributeValidator()


def distribute_match_influence(
    match_id,
    player_id,
    distributions,
):
    match_dict = match_gateway.get_match(match_id)
    match_dict = match_validator.match_exist(match_dict)

    match_validator.verify_match_status(match_dict, "running")
    match_validator.verify_current_turn_player_id(
        match_dict,
        player_id,
    )

    player = match_gateway.find_player(match_dict, player_id)
    player = player_validator.not_exist(player)

    match_influence = player["match_influence"]

    match_influence = (
        match_validator.verify_player_match_influence_is_not_below_zero(
            match_influence
        )
    )

    validated_distributions = (
        match_distribute_validator.distributions_are_valid(
            distributions=distributions,
            match_influence=match_influence,
            player_id=player_id,
            match_dict=match_dict,
        )
    )

    for distribution in validated_distributions:
        territory = distribution["territory"]
        distributed_influence = distribution["distributed_influence"]

        territory["current_influence"] += distributed_influence

    player["match_influence"] -= match_influence

    if (
        match_dict.get("phase") == "initial_distribution"
        and player["match_influence"] == 0
    ):
        match_factory.advance_turn(match_dict)

    match_factory.update_match(match_dict)

    return match_dict


def skip_turn_by_money_insufficient(match, action_result):
    skipped_player_id = match["current_turn_player_id"]
    match_factory.advance_turn(match)

    return {
        "match": match,
        "result": {
            **action_result,
            "next_turn_player_id": match["current_turn_player_id"],
            "round": match["round"],
            "winner_id": match.get("winner_id"),
            "status": match["status"],
            "skipped_player_id": skipped_player_id,
        },
    }


def initial_distribute_actions(
    match,
    available_attack_actions,
    available_defenses_actions,
):
    available_attack_actions = list(available_attack_actions)
    random.shuffle(available_attack_actions)

    available_attack_actions = match_action_factory.distribute_actions(
        available_attack_actions
    )

    match["round_attack_actions"] = available_attack_actions

    available_defenses_actions = list(available_defenses_actions)
    random.shuffle(available_defenses_actions)

    available_actions = match_action_factory.distribute_actions(
        available_defenses_actions
    )

    match["round_defense_actions"] = available_actions

    return match