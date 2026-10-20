from backend.app.validators.match_territory_validator import MatchTerritoryValidator
from backend.app.gateways.match_gateways import MatchGateway

class MatchDistributeValidator:

    def __init__(self):
        self.match_gateway = MatchGateway()
        self.match_territory_validator = MatchTerritoryValidator()

    def distribution_is_valid(
        self,
        distribution,
        player_id,
        match_dict,
    ):
        self.distribution_format_is_valid(distribution)

        distributed_influence = distribution["distributed_influence"]

        self.distributed_influence_is_valid(
            distributed_influence
        )

        territory = self.match_gateway.get_territory_by_id(
            match_dict,
            distribution["territory_id"],
        )

        territory = self.match_territory_validator.territory_exist(
            territory
        )

        self.match_territory_validator.verify_territory_owner_id(
            territory,
            player_id,
        )

        return distributed_influence

    def distributions_are_valid(
        self,
        distributions,
        match_influence,
        player_id,
        match_dict,
    ):
        self.distributions_exist(distributions)

        territory_ids = set()
        total_distributed_influence = 0

        for distribution in distributions:
            distributed_influence = self.distribution_is_valid(
                distribution,
                player_id,
                match_dict,
            )

            territory_id = distribution["territory_id"]

            self.territory_is_not_repeated(
                territory_id,
                territory_ids,
            )

            territory_ids.add(territory_id)
            total_distributed_influence += distributed_influence

        self.total_distributed_influence_is_on_limit(
            match_influence,
            total_distributed_influence,
        )

    def distributions_exist(self, distributions):
        if not isinstance(distributions, list) or not distributions:
            raise ValueError("Lista de distribuições inválida.")

    def distribution_format_is_valid(self, distribution):
        if not isinstance(distribution, dict):
            raise ValueError("Distribuição inválida.")

        if "territory_id" not in distribution:
            raise ValueError("ID do território não informado.")

        if "distributed_influence" not in distribution:
            raise ValueError("Quantidade de influência não informada.")

    def distributed_influence_is_valid(self, distributed_influence):
        if (
            isinstance(distributed_influence, bool)
            or not isinstance(distributed_influence, int)
            or distributed_influence <= 0
        ):
            raise ValueError(
                "A influência distribuída deve ser um inteiro positivo."
            )

    def total_distributed_influence_is_on_limit(
        self,
        match_influence,
        total_distributed_influence,
    ):
        if total_distributed_influence > match_influence:
            raise ValueError(
                "Você não possui influência suficiente para essa distribuição."
            )

    def territory_is_not_repeated(self, territory_id, territory_ids):
        if territory_id in territory_ids:
            raise ValueError(
                "Não é permitido distribuir influência duas vezes "
                "para o mesmo território."
            )