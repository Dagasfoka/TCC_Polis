from sqlalchemy.orm import Session

from backend.app.models.db.user import User
from backend.app.repositories.db.user_repo import UsersRepository


class UsersGateway:
    def __init__(self, db: Session):
        self.users_repository = UsersRepository(db)

    def get_all_users(self)-> list[User]:
        return self.users_repository.get_all_users()

    def get_user_by_id(self, user_id: int)-> list[User]:
            return self.users_repository.get_user_by_id(user_id)

    def get_user_by_username(self, username: str)-> list[User]:
            return self.users_repository.get_user_by_username(username)

    