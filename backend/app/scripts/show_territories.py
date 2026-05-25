from sqlalchemy import select

from backend.app.db.database import SessionLocal
from backend.app.models.database.territory_model import Territory


def show_territories() -> None:
    db = SessionLocal()

    try:
        territories =db.scalars(select(Territory)).all()
        for territory_data in territories:
            print(territory_data)
    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    show_territories()