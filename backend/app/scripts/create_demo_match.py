from backend.app.db.database import SessionLocal
from backend.app.repositories.redis.room_repo import save_room
from backend.app.services.redis.match_service import create_match

DEMO_ROOM_CODE = "DEMO1"


DEMO_ROOM = {
    "room_code": DEMO_ROOM_CODE,
    "players": [
        {
            "player_id": "p1",
            "username": "Redondo",
            "party_id": "PR",
        },
        {
            "player_id": "p2",
            "username": "Mexicano",
            "party_id": "PA",
        },
        {
            "player_id": "p3",
            "username": "Mínimo",
            "party_id": "PV",
        },
        {
            "player_id": "p4",
            "username": "Careca",
            "party_id": "PD",
        },
    ],
}


def create_demo_match():
    db = SessionLocal()

    save_room(DEMO_ROOM)

    match_dict = create_match(db, DEMO_ROOM_CODE)

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

    print("\nUse no HTML:")
    print(f"match_id = {match_dict['match_id']}")
    print("players = p1, p2, p3, p4")


if __name__ == "__main__":
    create_demo_match()