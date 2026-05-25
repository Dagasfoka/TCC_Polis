from backend.app.db.base import Base
from backend.app.db.database import SessionLocal, engine
from backend.app.models.database.party_model import Party

PARTIES = [
    {
        "id": "PR",
        "name": "Partido Rubro",
        "color": "#E74C3C",
    },
    {
        "id": "PA",
        "name": "Partido Azul",
        "color": "#3498DB",
    },
    {
        "id": "PV",
        "name": "Partido Verde",
        "color": "#2ECC71",
    },
    {
        "id": "PD",
        "name": "Partido Dourado",
        "color": "#F1C40F",
    },
]


def seed_parties():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        for party_data in PARTIES:
            party = Party(**party_data)
            db.merge(party)

        db.commit()

    print("Partidos criados/atualizados com sucesso.")


if __name__ == "__main__":
    seed_parties()