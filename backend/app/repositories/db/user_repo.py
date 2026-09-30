# Busca/salva usuários no banco.
from sqlalchemy import select
from backend.app.db.database import SessionLocal
from backend.app.api.deps import get_db
from backend.app.models.db.user import User

class UsersRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_users(self) -> list[User]:
        return list(self.db.scalars(select(User)).all())

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.scalar(
            select(User).where(User.username == username)
        )

    
    def create_user(self,username, password_hash):

        try:
            user = User(
                username=username,
                password_hash=password_hash,
                player_id=None
            )

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
    
            return {
                **user.to_dict(),
            }
            
        except Exception:
            self.db.rollback()
            raise