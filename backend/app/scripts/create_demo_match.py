from backend.app.db.database import SessionLocal
from backend.app.factories.room_factory import RoomFactory
from backend.app.services.redis.match_service import MatchService
from backend.app.factories.player_factory import PlayerFactory
from backend.app.db.redis import redis_client


DEMO_ROOM_CODE = "DEMO1"
match_service=MatchService ()

DEMO_PLAYERS = [
    {
        "username": "Redondo",
        "party_id": "PR",
    },
    {
        "username": "Mexicano",
        "party_id": "PA",
    },
    {
        "username": "Mínimo",
        "party_id": "PV",
    },
    {
        "username": "Careca",
        "party_id": "PD",
    },
]
player_factory=PlayerFactory()

def create_demo_match():
    db = SessionLocal()
    room_factory = RoomFactory()

    players = []

    for player_data in DEMO_PLAYERS:
        player = player_factory.create_player(
            username=player_data["username"],
            party_id=player_data["party_id"],
        )
        players.append(player)

    demo_room = {
        "room_code": DEMO_ROOM_CODE,
        "players": {}
    }

    for index, player in enumerate(players):
        demo_room["players"][player["player_id"]] = {
            "ready": index != 0,
            "host": index == 0,
        }

    room_factory.update_room(demo_room)

    match_dict = match_service.create_match(
        db,
        DEMO_ROOM_CODE,
    )

    print("Partida demo criada com sucesso.")
    print(f"room_code: {DEMO_ROOM_CODE}")
    print(f"match_id: {match_dict['match_id']}")
    print("\nPlayers:")

    for player in match_dict["players"]:
        print(
            f"- {player['player_id']} | "
            f"{player['username']} | "
            f"party_id={player['party_id']}"
        )

    return match_dict


if __name__ == "__main__":
    create_demo_match()