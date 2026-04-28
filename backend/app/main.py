from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect

from .schemas.base import Player

app = FastAPI()
templates = Jinja2Templates(directory='templates')
# servir arquivos estáticos
app.mount('/static', StaticFiles(directory='static'), name='static')

players = []


@app.get('/')
async def get_index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print('Novo jogador tentando conectar')
    player = Player(name='', websocket=websocket)
    players.append(player)

    try:
        print('Jogadore conectados: ', len(players))
        while True:
            data = await websocket.receive_text()
            player.name = data
            for p in players.copy():
                try:
                    await p.websocket.send_text(
                        player.name
                    )  # envia o nome do jogador para o navegador.
                except WebSocketDisconnect:
                    players.remove(p)
    except WebSocketDisconnect:
        players.remove(player)
