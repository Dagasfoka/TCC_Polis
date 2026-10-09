from sqlalchemy import select

from backend.app.db.database import SessionLocal
from backend.app.models.db.user import User


class UsersRepository:

    def get_all_users(self) -> list[User]:
        with SessionLocal() as db:
            users = list(
                db.scalars(
                    select(User)
                ).all()
            )

            return users


    def get_user_by_id(
        self,
        user_id: int
    ) -> User | None:

        with SessionLocal() as db:
            user = db.get(
                User,
                user_id
            )

            if user is not None:
                db.expunge(user)

            return user


    def get_user_by_username(
        self,
        username: str
    ) -> User | None:

        with SessionLocal() as db:
            user = db.scalar(
                select(User).where(
                    User.username == username
                )
            )

            if user is not None:
                db.expunge(user)

            return user


    def create_user(
        self,
        username,
        password_hash
    ):
        with SessionLocal() as db:
            try:
                user = User(
                    username=username,
                    password_hash=password_hash,
                    player_id=None
                )

                db.add(user)
                db.commit()
                db.refresh(user)

                return {
                    **user.to_dict(),
                }

            except Exception:
                db.rollback()
                raise


    def update_player_id(
        self,
        user_id: int,
        player_id: str | None
    ):
        with SessionLocal() as db:
            try:
                user = db.get(
                    User,
                    user_id
                )

                if user is None:
                    return None

                user.player_id = player_id

                db.commit()
                db.refresh(user)

                result = user.to_dict()

                return result

            except Exception:
                db.rollback()
                raise