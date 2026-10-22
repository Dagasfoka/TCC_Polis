from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, dict[str, WebSocket]] = {}

    async def connect(
        self,
        match_id: int,
        player_id: str,
        websocket: WebSocket,
    ):
        await websocket.accept()

        if match_id not in self.active_connections:
            self.active_connections[match_id] = {}

        # Guarda sempre a conexão mais recente do jogador
        self.active_connections[match_id][player_id] = websocket

    def disconnect(
        self,
        match_id: int,
        player_id: str,
        websocket: WebSocket,
    ):
        players = self.active_connections.get(match_id)

        if not players:
            return

        # Uma conexão antiga não pode remover a nova
        if players.get(player_id) is not websocket:
            return

        players.pop(player_id, None)

        if not players:
            self.active_connections.pop(match_id, None)

    async def send_to_player(
        self,
        match_id: int,
        player_id: str,
        message: dict,
    ):
        websocket = self.active_connections.get(
            match_id, {}
        ).get(player_id)

        if websocket is None:
            return

        try:
            await websocket.send_json(message)

        except Exception:
            logger.exception(
                "Erro ao enviar mensagem para jogador %s",
                player_id,
            )

            self.disconnect(
                match_id=match_id,
                player_id=player_id,
                websocket=websocket,
            )

    async def broadcast(
        self,
        match_id: int,
        message: dict,
    ):
        players = list(
            self.active_connections.get(match_id, {}).keys()
        )

        for player_id in players:
            await self.send_to_player(
                match_id=match_id,
                player_id=player_id,
                message=message,
            )

    async def send_to_all(
        self,
        match_id: int,
        message_factory,
    ):
        players = list(
            self.active_connections.get(match_id, {}).keys()
        )

        for player_id in players:
            await self.send_to_player(
                match_id=match_id,
                player_id=player_id,
                message=message_factory(player_id),
            )


manager = ConnectionManager()