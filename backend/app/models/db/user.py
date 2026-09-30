# Conta cadastrada.
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


from backend.app.db.base import Base


class User(Base):
    __tablename__ = "users"


    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )


    username: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )


    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )


    player_id: Mapped[str] = mapped_column(
        String,
        nullable=True,
        unique=True,
    )


    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "player_id": self.player_id,
        }
    


    def __repr__(self) -> str:
        return (
            f"User("
            f"user_id={self.user_id!r}, "
            f"username={self.username!r}, "
            f"player_id={self.player_id!r}"
            f")"
        )

