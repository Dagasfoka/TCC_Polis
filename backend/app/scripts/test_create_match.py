
from backend.app.db.database import SessionLocal
from backend.app.services.redis.match_service import create_match


def test_creat_match() -> None:
    db = SessionLocal()

    try:
        print(create_match(db))
    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    test_creat_match()