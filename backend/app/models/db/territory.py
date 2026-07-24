# Estado/território do mapa.
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Territory(Base):
    __tablename__ = "territories"

    id: Mapped[str] = mapped_column(String(2), primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    region: Mapped[str] = mapped_column(String(15), nullable=False)
    base_influence: Mapped[int] = mapped_column(Integer, nullable=False)
    def __repr__(self) -> str:
        return (
            f"Territory(id={self.id!r}, "
            f"name={self.name!r}, "
            f"region={self.region!r}, "
            f"base_influence={self.base_influence!r})"
        )