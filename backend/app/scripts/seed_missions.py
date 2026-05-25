from backend.app.db.base import Base
from backend.app.db.database import SessionLocal, engine
from backend.app.models.database.mission_model import Mission

MISSIONS = [
{
    "mission_id": 1,
    "type": "destruction",
    "content": {
        "destruction": None,
        "state": ["SP", "RJ", "MG", "BA", "PE", "CE"],
    },
},
{
    "mission_id": 2,
    "type": "state",
    "content": {
        "state": ["PR", "SC", "RS", "SP", "RJ", "MG"],
    },
},
    {
        "mission_id": 3,
        "type": "region",
        "content": {
            "region": [
                {
                    "region": "Nordeste",
                    "quantity": 3,
                },
                {
                    "region": "Sul",
                    "quantity": 1,
                },
            ],
        },
    },
    {
        "mission_id": 4,
        "type": "region",
        "content": {
            "region": [
                {
                    "region": "Centro-Oeste",
                    "quantity": 2,
                },
                {
                    "region": "Sudeste",
                    "quantity": 2,
                },
            ],
        },
    },
]


def seed_missions():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        for mission_data in MISSIONS:
            mission = Mission(**mission_data)
            db.merge(mission)

        db.commit()

    print("Missões criadas/atualizadas com sucesso.")


if __name__ == "__main__":
    seed_missions()
    