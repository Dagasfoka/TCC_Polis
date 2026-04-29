from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from backend.app.websocket.manager import manager

router = APIRouter()


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
