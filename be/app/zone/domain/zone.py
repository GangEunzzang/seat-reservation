from typing import Optional

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.entity.base_entity import Timestamp
from core.config.database import Base


class Zone(Base, Timestamp):
	__tablename__ = "zone"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	episode_id: Mapped[int] = mapped_column(Integer, nullable=False)
	code: Mapped[str] = mapped_column(String(10), nullable=False)  # 'A', 'B', 'C', 'D'
	name: Mapped[str] = mapped_column(String(100), nullable=False)  # '메인홀', 'VIP룸'

	@classmethod
	def create(cls, episode_id: int, code: str, name: str) -> "Zone":
		"""Zone 생성"""
		return cls(
			episode_id=episode_id,
			code=code,
			name=name,
		)

	def update_name(self, name: str) -> None:
		"""Zone 이름 수정"""
		self.name = name
