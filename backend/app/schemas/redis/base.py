from dataclasses import dataclass

from fastapi import WebSocket

# from uuid import uuid4 (futuro)


@dataclass
class Player:
    name: str
    websocket: WebSocket
