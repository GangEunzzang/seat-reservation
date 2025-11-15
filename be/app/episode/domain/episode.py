from datetime import date

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.entity.base_entity import Timestamp
from core.config.database import Base


class Episode(Base, Timestamp):
	__tablename__ = "episode"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	year: Mapped[int] = mapped_column(Integer, nullable=False)
	name: Mapped[str] = mapped_column(nullable=False)
	start_date: Mapped[date] = mapped_column(nullable=False)
	end_date: Mapped[date] = mapped_column(nullable=False)

	@classmethod
	def create(cls, year: int, name: str, start_date: date, end_date: date) -> "Episode":
		return cls(
			year=year,
			name=name,
			start_date=start_date,
			end_date=end_date,
		)
