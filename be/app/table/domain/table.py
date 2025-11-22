from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.config.database import Base
from core.entity.base_entity import Timestamp


class Table(Base, Timestamp):
	__tablename__ = "table"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	episode_id: Mapped[int] = mapped_column(Integer, nullable=False)
	zone_id: Mapped[int] = mapped_column(Integer, nullable=False)
	x: Mapped[int] = mapped_column(Integer, nullable=False)
	y: Mapped[int] = mapped_column(Integer, nullable=False)
	name: Mapped[str] = mapped_column(String(100), nullable=False)

	@classmethod
	def create(cls, episode_id: int, zone_id: int, x: int, y: int, name: str) -> "Table":
		return cls(
			episode_id=episode_id,
			zone_id=zone_id,
			x=x,
			y=y,
			name=name,
		)

	def update_position(self, x: int, y: int) -> None:
		"""테이블 위치 수정"""
		self.x = x
		self.y = y
