from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from backend.app.api.routes.routes import router as api_router

from backend.app.utils.room_exceptions import (
    RoomNotFoundError,
    RoomFullError,
    PlayerAlreadyInRoomError,
    OnlyHostError,
    PlayerNotInRoomError,
    RoomNotReadyError,
    PartyUnavailableError,
)


app = FastAPI()


# ==============================
# TRATAMENTO GLOBAL DE EXCEPTIONS
# ==============================

@app.exception_handler(RoomNotFoundError)
async def room_not_found_handler(
    request: Request,
    exc: RoomNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        }
    )


@app.exception_handler(RoomFullError)
async def room_full_handler(
    request: Request,
    exc: RoomFullError
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        }
    )


@app.exception_handler(PlayerAlreadyInRoomError)
async def player_already_in_room_handler(
    request: Request,
    exc: PlayerAlreadyInRoomError
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        }
    )


@app.exception_handler(OnlyHostError)
async def only_host_handler(
    request: Request,
    exc: OnlyHostError
):
    return JSONResponse(
        status_code=403,
        content={
            "detail": str(exc)
        }
    )


@app.exception_handler(PlayerNotInRoomError)
async def player_not_in_room_handler(
    request: Request,
    exc: PlayerNotInRoomError
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        }
    )


@app.exception_handler(RoomNotReadyError)
async def room_not_ready_handler(
    request: Request,
    exc: RoomNotReadyError
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        }
    )


@app.exception_handler(PartyUnavailableError)
async def party_unavailable_handler(
    request: Request,
    exc: PartyUnavailableError
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        }
    )


# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "https://frontend-ytma.onrender.com",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# FRONTEND ESTÁTICO
# ==============================

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)


# ==============================
# ROTAS
# ==============================

app.include_router(api_router)