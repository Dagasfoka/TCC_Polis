# Dependências reutilizáveis das rotas.

from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.app.db.database import SessionLocal


def get_db() -> Generator[Session]: #Utils
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()