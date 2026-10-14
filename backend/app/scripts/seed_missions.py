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
            "state": ["AM", "PA", "MT"],
        },
    },
    {
        "mission_id": 2,
        "type": "state",
        "content": {
            "state": ["SP", "RJ", "MG", "BA"],
        },
    },
    {
        "mission_id": 3,
        "type": "state",
        "content": {
            "state": ["AC", "RO", "AM", "MT"],
        },
    },
    {
        "mission_id": 4,
        "type": "region",
        "content": {
            "region": [
                {
                    "region": "Centro-Oeste",
                    "quantity": 3,
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