from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Seat(Base):
    __tablename__ = "seat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    episode_id: Mapped[int] = mapped_column(Integer, nullable=False)

    @classmethod
    def create(cls, episode_id: int) -> "Seat":
        return cls(
            episode_id=episode_id,
        )

