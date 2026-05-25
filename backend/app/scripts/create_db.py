from backend.app.db.base import Base
from backend.app.db.database import engine


def create_database() -> None:
    Base.metadata.create_all(bind=engine)
    print("Banco criado com sucesso.")


if __name__ == "__main__":
    create_database()