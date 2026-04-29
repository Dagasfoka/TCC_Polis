from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes import router as api_router
from backend.app.websocket.routes import router as websocket_router

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(api_router)
app.include_router(websocket_router)
