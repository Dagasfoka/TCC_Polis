# Busca/salva usuários no banco.
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.db.user import User

class UsersRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_all_users(self) -> list[User]:
        return list(self.db.scalars(select(User)).all())

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.scalar(
            select(User).where(User.username == username)
        )

    
    def create_user(self,username, password_hash):

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