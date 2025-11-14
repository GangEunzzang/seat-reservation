from typing import Optional

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_entity import Timestamp
from app.core.database import Base
from app.domain.user.domain.user_register_request import UserRegisterRequest


class User(Base, Timestamp):
	__tablename__ = "user"

	id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, autoincrement=True)
	user_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
	name: Mapped[str] = mapped_column(String(100), nullable=False)
	department: Mapped[str] = mapped_column(String(100), nullable=False)
	position: Mapped[str] = mapped_column(String(100), nullable=False)
	phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
	episode_id: Mapped[int] = mapped_column(Integer, nullable=False)

	@classmethod
	def create(cls, register_request: UserRegisterRequest) -> "User":
		return cls(
			user_code=register_request.user_code,
			name=register_request.name,
			department=register_request.department,
			position=register_request.position,
			phone_number=register_request.phone_number,
			episode_id=register_request.episode_id,
		)
