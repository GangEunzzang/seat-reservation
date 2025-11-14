from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_entity import Timestamp
from app.core.database import Base


class Table(Base, Timestamp):
	__tablename__ = "table"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	episode_id: Mapped[int] = mapped_column(Integer, nullable=False)

	@classmethod
	def create(cls, episode_id: int) -> "Table":
		return cls(
			episode_id=episode_id,
		)
