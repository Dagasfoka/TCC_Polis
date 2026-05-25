from fastapi import WebSocket


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

        self.active_connections[match_id][player_id] = websocket

    def disconnect(
        self,
        match_id: int,
        player_id: str,
    ):
        if match_id not in self.active_connections:
            return

        self.active_connections[match_id].pop(player_id, None)

        if not self.active_connections[match_id]:
            self.active_connections.pop(match_id, None)

    async def send_to_player(
        self,
        match_id: int,
        player_id: str,
        message: dict,
    ):
        websocket = self.active_connections.get(match_id, {}).get(player_id)

        if websocket is None:
            return

        await websocket.send_json(message)

    async def broadcast(
        self,
        match_id: int,
        message: dict,
    ):
        players = self.active_connections.get(match_id, {})

        for websocket in players.values():
            await websocket.send_json(message)


manager = ConnectionManager()