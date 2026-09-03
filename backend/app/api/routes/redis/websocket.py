from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.app.repositories.redis.match_repo import get_match_state
from backend.app.services.db.action_service import (
    get_attack_options,
    resolve_attack_option,
    resolve_attack_question,
)
from backend.app.websocket.manager import manager

router_websocket = APIRouter()


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
    match_for_player["available_attack_options"] = get_attack_options()

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
        match = get_match_state(match_id)

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

                response = resolve_attack_option(
                    match_id=match_id,
                    player_id=player_id,
                    target_territory_id=target_territory_id,
                    option_id=option_id,
                )

                await manager.send_to_player(
                    match_id=match_id,
                    player_id=player_id,
                    message=response["result"],
                )

            elif event_type == "answer_attack_question":
                answer = data.get("answer")

                if answer is None:
                    answer = payload.get("answer")

                response = resolve_attack_question(
                    match_id=match_id,
                    player_id=player_id,
                    answer=answer,
                )

                updated_match = response["match"]

                players = manager.active_connections.get(match_id, {})
                
                for connected_player_id in players.keys():
                    await manager.send_to_player(
                        match_id=match_id,
                        player_id=connected_player_id,
                        message={
                            "type": "match_state",
                            "payload": prepare_match_for_player(
                                updated_match,
                                connected_player_id,
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

    except WebSocketDisconnect:
        manager.disconnect(
            match_id=match_id,
            player_id=player_id,
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

        manager.disconnect(
            match_id=match_id,
            player_id=player_id,
        )
