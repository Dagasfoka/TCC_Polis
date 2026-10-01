from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.app.gateways.match_gateways import MatchGateway
from backend.app.services.redis.action_service import (
    get_attack_actions,
    prepare_attack_action,
    resolve_attack_action,
)
from backend.app.websocket.manager import manager

router_websocket = APIRouter()

match_gateway=MatchGateway()
def find_your_mission(match: dict, player_id: str):
    missions = match.get("missions", [])

    for mission in missions:
        if mission.get("owner_id") == player_id:
            return mission.get("mission") or mission

    return None


def prepare_match_for_player(match: dict, player_id: str):
    match_for_player = match.copy()

    match_for_player["your_player_id"] = player_id
    match_for_player["your_mission"] = find_your_mission(match, player_id)
    match_for_player["available_attack_options"] = get_attack_actions()

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

                    option_id = data.get("option_id") or payload.get("option_id")

                    response = prepare_attack_action(
                        match_id=match_id,
                        player_id=player_id,
                        target_territory_id=target_territory_id,
                        option_id=option_id,
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

                elif event_type == "answer_attack_question":
                    answer = data.get("answer")

                    if answer is None:
                        answer = payload.get("answer")

                    response = resolve_attack_action(
                        match_id=match_id,
                        player_id=player_id,
                        answer=answer,
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