# backend/scripts/seed_territories.py

from sqlalchemy import select

from backend.app.db.database import SessionLocal
from backend.app.models.database.territory_model import Territory

TERRITORIES_DATA = [
    # Norte
    {"id": "AC", "name": "Acre", "region": "Norte", "base_influence": 3},
    {"id": "AM", "name": "Amazonas", "region": "Norte", "base_influence": 5},
    {"id": "PA", "name": "Pará", "region": "Norte", "base_influence": 5},
    {"id": "RO", "name": "Rondônia", "region": "Norte", "base_influence": 3},
    {"id": "TO", "name": "Tocantins", "region": "Norte", "base_influence": 3},

    # Nordeste
    {"id": "AL", "name": "Alagoas", "region": "Nordeste", "base_influence": 3},
    {"id": "BA", "name": "Bahia", "region": "Nordeste", "base_influence": 6},
    {"id": "CE", "name": "Ceará", "region": "Nordeste", "base_influence": 5},
    {"id": "MA", "name": "Maranhão", "region": "Nordeste", "base_influence": 4},
    {"id": "PE", "name": "Pernambuco", "region": "Nordeste", "base_influence": 5},
    {"id": "PI", "name": "Piauí", "region": "Nordeste", "base_influence": 3},

    # Centro-Oeste
    {"id": "DF", "name": "Distrito Federal", "region": "Centro-Oeste", "base_influence": 6},
    {"id": "GO", "name": "Goiás", "region": "Centro-Oeste", "base_influence": 4},
    {"id": "MT", "name": "Mato Grosso", "region": "Centro-Oeste", "base_influence": 4},
    {"id": "MS", "name": "Mato Grosso do Sul", "region": "Centro-Oeste", "base_influence": 4},

    # Sudeste
    {"id": "MG", "name": "Minas Gerais", "region": "Sudeste", "base_influence": 7},
    {"id": "RJ", "name": "Rio de Janeiro", "region": "Sudeste", "base_influence": 7},
    {"id": "SP", "name": "São Paulo", "region": "Sudeste", "base_influence": 9},

    # Sul
    {"id": "PR", "name": "Paraná", "region": "Sul", "base_influence": 6},
    {"id": "SC", "name": "Santa Catarina", "region": "Sul", "base_influence": 5},
]


def seed_territories() -> None:
    db = SessionLocal()

    try:
        for territory_data in TERRITORIES_DATA:
            territory_id = territory_data["id"]

            existing_territory = db.scalar(
                select(Territory).where(Territory.id == territory_id)
            )

            if existing_territory is not None:
                continue

            territory = Territory(**territory_data)
            db.add(territory)

        db.commit()
        print("Territórios inseridos com sucesso.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_territories()