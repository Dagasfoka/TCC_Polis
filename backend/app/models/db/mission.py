from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Mission(Base):
    __tablename__ = "missions"

    mission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    content: Mapped[dict] = mapped_column(JSON, nullable=False)

    def to_dict(self) -> dict:
        return {
            "mission_id": self.mission_id,
            "type": self.type,
            "content": self.content,
        }

    def __repr__(self) -> str:
        return (
            f"Mission("
            f"mission_id={self.mission_id!r}, "
            f"type={self.type!r}, "
            f"content={self.content!r}"
            f")"
        )