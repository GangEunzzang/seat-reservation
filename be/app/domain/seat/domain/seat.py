from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_entity import Timestamp
from app.core.database import Base


class Seat(Base, Timestamp):
	__tablename__ = "seat"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	table_id: Mapped[int] = mapped_column(Integer, nullable=False)
	seat_number: Mapped[int] = mapped_column(Integer, nullable=False)

	@classmethod
	def create(cls, table_id: int, seat_number: int) -> "Seat":
		return cls(
			table_id=table_id,
			seat_number=seat_number,
		)
