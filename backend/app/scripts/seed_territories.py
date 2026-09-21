# backend/scripts/seed_territories.py

from sqlalchemy import select

from backend.app.db.database import SessionLocal
from backend.app.models.db.territory import Territory


TERRITORIES_DATA = [
    # Norte
    {
        "id": "AC",
        "name": "Acre",
        "region": "Norte",
        "base_influence": 3,
        "frontiers": ["AM", "RO", "SC"],  # SC = fronteira especial
    },
    {
        "id": "AM",
        "name": "Amazonas",
        "region": "Norte",
        "base_influence": 5,
        "frontiers": ["AC", "RO", "MT", "PA"],
    },
    {
        "id": "PA",
        "name": "Pará",
        "region": "Norte",
        "base_influence": 5,
        "frontiers": ["AM", "MT", "TO", "MA"],
    },
    {
        "id": "RO",
        "name": "Rondônia",
        "region": "Norte",
        "base_influence": 3,
        "frontiers": ["AC", "AM", "MT"],
    },
    {
        "id": "TO",
        "name": "Tocantins",
        "region": "Norte",
        "base_influence": 3,
        "frontiers": ["PA", "MA", "PI", "BA", "GO", "MT"],
    },

    # Nordeste
    {
        "id": "AL",
        "name": "Alagoas",
        "region": "Nordeste",
        "base_influence": 3,
        "frontiers": ["PE", "BA"],
    },
    {
        "id": "BA",
        "name": "Bahia",
        "region": "Nordeste",
        "base_influence": 6,
        "frontiers": ["AL", "PE", "PI", "TO", "GO", "MG", "RJ"],
    },
    {
        "id": "CE",
        "name": "Ceará",
        "region": "Nordeste",
        "base_influence": 5,
        "frontiers": ["PI", "PE", "RJ"],  # RJ = fronteira especial
    },
    {
        "id": "MA",
        "name": "Maranhão",
        "region": "Nordeste",
        "base_influence": 4,
        "frontiers": ["PA", "TO", "PI"],
    },
    {
        "id": "PE",
        "name": "Pernambuco",
        "region": "Nordeste",
        "base_influence": 5,
        "frontiers": ["CE", "PI", "BA", "AL"],
    },
    {
        "id": "PI",
        "name": "Piauí",
        "region": "Nordeste",
        "base_influence": 3,
        "frontiers": ["MA", "CE", "PE", "BA", "TO"],
    },

    # Centro-Oeste
    {
        "id": "DF",
        "name": "Distrito Federal",
        "region": "Centro-Oeste",
        "base_influence": 6,
        "frontiers": ["GO", "MG"],
    },
    {
        "id": "GO",
        "name": "Goiás",
        "region": "Centro-Oeste",
        "base_influence": 4,
        "frontiers": ["TO", "BA", "MG", "MS", "MT", "DF"],
    },
    {
        "id": "MT",
        "name": "Mato Grosso",
        "region": "Centro-Oeste",
        "base_influence": 4,
        "frontiers": ["RO", "AM", "PA", "TO", "GO", "MS"],
    },
    {
        "id": "MS",
        "name": "Mato Grosso do Sul",
        "region": "Centro-Oeste",
        "base_influence": 4,
        "frontiers": ["MT", "GO", "MG", "SP", "PR"],
    },

    # Sudeste
    {
        "id": "MG",
        "name": "Minas Gerais",
        "region": "Sudeste",
        "base_influence": 7,
        "frontiers": ["BA", "GO", "DF", "MS", "SP", "RJ"],
    },
    {
        "id": "RJ",
        "name": "Rio de Janeiro",
        "region": "Sudeste",
        "base_influence": 7,
        "frontiers": ["MG", "SP", "BA", "CE"],  # CE = fronteira especial
    },
    {
        "id": "SP",
        "name": "São Paulo",
        "region": "Sudeste",
        "base_influence": 9,
        "frontiers": ["MG", "RJ", "MS", "PR"],
    },

    # Sul
    {
        "id": "PR",
        "name": "Paraná",
        "region": "Sul",
        "base_influence": 6,
        "frontiers": ["SP", "MS", "SC"],
    },
    {
        "id": "SC",
        "name": "Santa Catarina",
        "region": "Sul",
        "base_influence": 5,
        "frontiers": ["PR", "AC"],  # AC = fronteira especial
    },
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
                existing_territory.frontiers = territory_data["frontiers"]
                continue

            territory = Territory(**territory_data)
            db.add(territory)

        db.commit()
        print("Territórios inseridos/atualizados com sucesso.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_territories()
