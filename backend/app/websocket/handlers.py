from backend.app.services.action_service import resolve_attack_option


async def handle_match_message(match_id: int, player_id: str, data: dict):
    event_type = data.get("type")
    payload = data.get("payload", {})

    if event_type == "attack_territory":
        target_territory_id = payload["territory_id"]
        option_id = payload["option_id"]

        action_response = resolve_attack_option(
            match_id=match_id,
            player_id=player_id,
            target_territory_id=target_territory_id,
            option_id=option_id,
        )

        return action_response["match"]

    raise ValueError(f"Evento inválido: {event_type}")