from backend.app.factories.match_action_factory import MatchActionFactory
from backend.app.validators.match_validators import MatchValidator
from backend.app.gateways.match_gateways import MatchGateway
from backend.app.validators.player_validators import PlayerValidator
from backend.app.validators.match_territory_validator import MatchTerritoryValidator
from backend.app.factories.match_factory import MatchFactory
import random


match_territory_validator = MatchTerritoryValidator()
match_factory = MatchFactory()
match_validator = MatchValidator()
match_gateway = MatchGateway()
player_validator = PlayerValidator()
match_action_factory = MatchActionFactory()


def distribute_match_influence(
    match_id,
    player_id,
    distributions,
):
    match_dict = match_gateway.get_match(match_id)
    match_dict = match_validator.match_exist(match_dict)
    match_validator.verify_match_status(match_dict, "running")
    match_validator.verify_current_turn_player_id(match_dict, player_id)

    player = match_gateway.find_player(match_dict, player_id)
    player = player_validator.not_exist(player)

    match_influence = player["match_influence"]
    match_influence = (
        match_validator.verify_player_match_influence_is_not_below_zero(
            match_influence
        )
    )

    if not isinstance(distributions, list) or not distributions:
        raise ValueError("Lista de distribuições inválida.")

    territory_ids = set()
    validated_distributions = []
    total_distributed_influence = 0

    # Primeira passagem: validar toda a lista sem modificar a partida.
    for distribution in distributions:
        if not isinstance(distribution, dict):
            raise ValueError("Distribuição inválida.")

        if "territory_id" not in distribution:
            raise ValueError("ID do território não informado.")

        if "distributed_influence" not in distribution:
            raise ValueError("Quantidade de influência não informada.")

        territory_id = distribution["territory_id"]
        distributed_influence = distribution["distributed_influence"]

        if (
            isinstance(distributed_influence, bool)
            or not isinstance(distributed_influence, int)
            or distributed_influence <= 0
        ):
            raise ValueError(
                "A influência distribuída deve ser um inteiro positivo."
            )

        # IDs iguais não devem aparecer duas vezes, mesmo que um venha
        # como string e o outro como inteiro.
        normalized_territory_id = str(territory_id)

        if normalized_territory_id in territory_ids:
            raise ValueError(
                "Não é permitido distribuir influência duas vezes "
                "para o mesmo território."
            )

        territory_ids.add(normalized_territory_id)

        territory = match_gateway.get_territory_by_id(
            match_dict,
            territory_id,
        )
        territory = match_territory_validator.territory_exist(territory)

        match_territory_validator.verify_territory_owner_id(
            territory,
            player_id,
        )

        total_distributed_influence += distributed_influence

        validated_distributions.append(
            {
                "territory": territory,
                "distributed_influence": distributed_influence,
            }
        )

    if total_distributed_influence > match_influence:
        raise ValueError(
            "Você não possui influência suficiente para essa distribuição."
        )

    # Segunda passagem: somente depois de validar tudo, aplicar as mudanças.
    for distribution in validated_distributions:
        territory = distribution["territory"]
        distributed_influence = distribution["distributed_influence"]

        territory["current_influence"] += distributed_influence

    player["match_influence"] -= total_distributed_influence

    if (
        match_dict.get("phase") == "initial_distribution"
        and player["match_influence"] == 0
    ):
        match_factory.advance_turn(match_dict)

    # Persiste a partida uma única vez.
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