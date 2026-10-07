from backend.app.db.base import Base
from backend.app.db.database import engine
from backend.app.models.db.action import Action
from backend.app.models.db.mission import Mission
from backend.app.models.db.party import Party
from backend.app.models.db.territory import Territory
from backend.app.db.redis import redis_client

def create_database() -> None:
    Base.metadata.create_all(bind=engine)
    redis_client.flushall()
    print("Banco criado com sucesso.")
    print("Redis limpo com sucesso.")


if __name__ == "__main__":
    create_database()