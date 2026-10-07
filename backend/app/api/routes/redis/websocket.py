from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import random

from backend.app.gateways.match_gateways import MatchGateway
from backend.app.services.redis.action_service import (
    prepare_attack_action,
    resolve_attack_action,
    get_match_attack_actions,
    get_match_defense_actions,
    distribute_actions
)

from backend.app.validators.db.territory_validator import TerritoryValidator
from backend.app.websocket.manager import manager

router_websocket = APIRouter()

match_gateway=MatchGateway()
territory_validator=TerritoryValidator()

def prepare_match_for_player(match: dict, player_id: str):
    match_for_player = match.copy()
    match_for_player["your_player_id"] = player_id
    match_for_player["your_mission"] = match_gateway.find_your_mission(match, player_id)
    match_for_player["available_attack_options"] = get_match_attack_actions(match["match_id"])
    match_for_player["available_defense_options"] = get_match_defense_actions(match["match_id"])

    return match_for_player

@router_websocket.websocket("/ws/match/{match_id}/{player_id}")
async def match_websocket(
    websocket: WebSocket,
    match_id: int,
    player_id: str,
):
    await manager.connect(
        match_id=match_id,
        player_id=player_id,
        websocket=websocket,
    )

    try:
        match = match_gateway.get_match(match_id)

        if match is None:
            await manager.send_to_player(
                match_id=match_id,
                player_id=player_id,
                message={
                    "type": "error",
                    "payload": {
                        "message": "Partida não encontrada.",
                    },
                },
            )
            return

        await manager.send_to_player(
            match_id=match_id,
            player_id=player_id,
            message={
                "type": "match_state",
                "payload": prepare_match_for_player(match, player_id),
            },
        )

        while True:
            data = await websocket.receive_json()

            try:
                event_type = data.get("type")
                payload = data.get("payload", {})


                if event_type == "choose_attack_option":
                    target_territory_id = (
                        data.get("target_territory_id")
                        or data.get("territory_id")
                        or payload.get("target_territory_id")
                        or payload.get("territory_id")
                    )

                    option_id = data.get("action_id") or payload.get("action_id")
                    action_type = data.get("action_type") or payload.get("action_type")

                    response = prepare_attack_action(
                        match_id=match_id,
                        player_id=player_id,
                        target_territory_id=target_territory_id,
                        option_id=option_id,
                        action_type=action_type
                    )

                    if response["result"]["type"] == "attack_question":
                        await manager.send_to_player(
                            match_id=match_id,
                            player_id=player_id,
                            message=response["result"],
                        )
                    elif response['result']['type'] == "attack_no_question":
                        updated_match = response["match"]

                        await manager.send_to_all(
                            match_id,
                            lambda recipient_id: {
                                "type": "match_state",
                                "payload": prepare_match_for_player(
                                    updated_match,
                                    recipient_id,
                                ),
                            },
                        )

                elif event_type == "select_territory":
                    territory_id = (
                        data.get("territory_id")
                        or payload.get("territory_id")
                    )

                    match = match_gateway.get_match(match_id)

                    territory = match_gateway.get_territory_by_id(
                        match,
                        territory_id,
                    )
                    territory=territory_validator.territory_exist(territory)

                    owner_id = territory["owner_id"]

                    is_my_territory = owner_id == player_id

                    action_type = "defense" if is_my_territory else "attack"
                    available_actions = get_match_defense_actions(match_id) if is_my_territory else get_match_attack_actions(match_id)
                    random.shuffle(available_actions)
                    player_available_actions = distribute_actions(available_actions)

                    await manager.send_to_player(
                        match_id=match_id,
                        player_id=player_id,
                        message={
                            "type": "territory_selected",
                            "payload": {
                                "action_type": action_type,
                                "territory": territory,
                                "available_actions": player_available_actions,
                            },
                        },
                    )

                elif event_type == "answer_attack_question":
                    answer = data.get("answer")

                    if answer is None:
                        answer = payload.get("answer")

                    response = resolve_attack_action(
                        match_id=match_id,
                        player_id=player_id,
                        answer=answer,
                        action_type="attack"
                    )

                    updated_match = response["match"]

                    await manager.send_to_all(
                        match_id,
                        lambda player_id: {
                            "type": "match_state",
                            "payload": prepare_match_for_player(
                                updated_match,
                                player_id,
                            ),
                        },
                    )

                else:
                    await manager.send_to_player(
                        match_id=match_id,
                        player_id=player_id,
                        message={
                            "type": "error",
                            "payload": {
                                "message": f"Evento WebSocket desconhecido: {event_type}",
                            },
                        },
                    )

            except Exception as error:
                await manager.send_to_player(
                    match_id=match_id,
                    player_id=player_id,
                    message={
                        "type": "error",
                        "payload": {
                            "message": str(error),
                        },
                    },
                )
    except WebSocketDisconnect:
        manager.disconnect(
            match_id=match_id,
            player_id=player_id,
        )