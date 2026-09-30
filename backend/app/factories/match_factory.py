from backend.app.factories.match_territory_factory import MatchTerritoryFactory
from backend.app.repositories.redis.match_repo import MatchRepo
from backend.app.repositories.db.territory_repo import TerritoryRepo
from backend.app.gateways.player_gateways import PlayerGateway
from backend.app.models.redis.match import Match
class MatchFactory:
    def __init__(self) -> None:
        self.match_repository=MatchRepo()
        self.territory_repo=TerritoryRepo()
        self.player_gateway=PlayerGateway()
        self.match_territory_factory= MatchTerritoryFactory()
    def update_match(self,match_dict):
        return self.match_repository.update_match(match_dict)
    def build_initial_match_state(self, db, room_dict) -> dict:
        territories = self.territory_repo.get_all_territories(db)
        match_territories = []
        match_id = self.match_repository.generate_match_id()

        for territory_data in territories:
            match_territory = self.match_territory_factory.build_match_territory(
                match_id,
                territory_data,
            )
            match_territories.append(match_territory)

        players_ids = room_dict["players"].keys()

    # Busca os dados dos jogadores
        match_players = self.player_gateway.get_players(players_ids)

    # Copia o partido escolhido no lobby para o jogador da partida
        for match_player in match_players:
            player_id = match_player["player_id"]

            room_player = room_dict["players"].get(player_id)

            if room_player is None:
                raise ValueError(
                    f"Jogador {player_id} não encontrado na sala"
                )

            party_id = room_player.get("party_id")

            if party_id is None:
                raise ValueError(
                    f"Jogador {player_id} não escolheu um partido"
                )

            match_player["party_id"] = party_id

        match_dict = Match.create_dict(
            match_id=match_id,
            territories=match_territories,
            room_code=room_dict["room_code"],
            players=match_players,
            status="running",
            current_turn_player_id=next(iter(room_dict["players"])),
            round=1,
            missions=[],
            )

        return match_dict