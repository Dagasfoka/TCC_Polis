import random

from backend.app.gateways.missions_gateways import MissionsGateway
from backend.app.gateways.match_gateways import MatchGateway
from backend.app.gateways.questions_gateways import QuestionGateways

from backend.app.rules.missions_rules import MissionsRules

from backend.app.models.redis.match import Match
from backend.app.models.redis.match_territory import MatchTerritory
from backend.app.repositories.redis.match_repo import generate_match_id
from backend.app.repositories.db.territory_repo import get_all_territories



def build_initial_match_state(db, room_dict) -> Match:
    territories = get_all_territories(db)
    match_territories = []
    match_id = generate_match_id()

    for territory_data in territories:
        match_territory = MatchTerritory(
            match_id=match_id,
            territory_id=territory_data.id,
            base_influence=territory_data.base_influence,
            name=territory_data.name,
            region=territory_data.region,
        )
        match_territories.append(match_territory)
    match_state = Match(
        match_id=match_id,
        territories=match_territories,
        room_code=room_dict["room_code"],
        players=room_dict["players"],
        status="running",
        current_turn_player_id=room_dict["players"][0]["player_id"],
        round=1,
        missions=[],
    )

    return match_state


