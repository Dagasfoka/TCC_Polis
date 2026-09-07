from backend.app.db.base import Base
from backend.app.db.database import engine
from backend.app.models.db.action_option import ActionOption
from backend.app.models.db.mission import Mission
from backend.app.models.db.party import Party
from backend.app.models.db.territory import Territory


def create_database() -> None:
    Base.metadata.create_all(bind=engine)
    print("Banco criado com sucesso.")


if __name__ == "__main__":
    create_database()