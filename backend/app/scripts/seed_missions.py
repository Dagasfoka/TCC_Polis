from sqlalchemy import delete

from backend.app.db.base import Base
from backend.app.db.database import SessionLocal, engine
from backend.app.models.db.mission import Mission

MISSIONS = [
    {
        "mission_id": 1,
        "type": "destruction",
        "content": {
            "destruction": None,

            # Missão alternativa caso a destruição seja convertida.
            "state": ["AM", "PA"],
        },
    },
    {
        "mission_id": 2,
        "type": "state",
        "content": {
            "state": ["SP", "RJ"],
        },
    },
    {
        "mission_id": 3,
        "type": "state",
        "content": {
            "state": ["AC", "RO"],
        },
    },
    {
        "mission_id": 4,
        "type": "region",
        "content": {
            "region": [
                {
                    "region": "Sul",
                    "quantity": 2,
                },
            ],
        },
    },
]

def seed_missions():
    Base.metadata.create_all(bind=engine)

    with SessionLocal.begin() as db:
        # Apaga todas as missões antigas.
        db.execute(delete(Mission))

        missions = [
            Mission(**mission_data)
            for mission_data in MISSIONS
        ]

        db.add_all(missions)

    print("Missões antigas apagadas.")
    print("Missões de demonstração criadas com sucesso.")


if __name__ == "__main__":
    seed_missions()