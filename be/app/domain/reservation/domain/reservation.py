from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_entity import Timestamp
from app.core.database import Base
from app.domain.reservation.domain.reservation_status import ReservationStatus

class Reservation(Base, Timestamp):
	__tablename__ = "reservation"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	user_id: Mapped[int] = mapped_column(Integer, nullable=False)
	seat_id: Mapped[int] = mapped_column(Integer, nullable=False)
	status: Mapped[str] = mapped_column(String(20), nullable=False, default=ReservationStatus.RESERVED.code)
	reserved_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
	cancelled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

	# 활성 예약(RESERVED)만 seat_id가 unique하도록 제약
	__table_args__ = (
		Index(
			'idx_unique_active_seat',
			'seat_id',
			unique=True,
			postgresql_where=(status == ReservationStatus.RESERVED.code)
		),
	)

	@classmethod
	def create(cls, user_id: int, seat_id: int) -> "Reservation":
		"""예약 생성"""
		return cls(
			user_id=user_id,
			seat_id=seat_id,
			status=ReservationStatus.RESERVED.code,
			reserved_at=datetime.now(),
			cancelled_at=None,
		)

	def cancel(self) -> None:
		"""예약 취소"""
		if self.get_status() == ReservationStatus.CANCELLED:
			raise ValueError("Already cancelled reservation")

		self.status = ReservationStatus.CANCELLED.code
		self.cancelled_at = datetime.now()

	def get_status(self) -> ReservationStatus:
		"""상태를 Enum으로 반환"""
		return ReservationStatus.from_code(self.status)

	def is_active(self) -> bool:
		"""활성 예약인지 확인"""
		return self.get_status() == ReservationStatus.RESERVED

	def is_cancelled(self) -> bool:
		"""취소된 예약인지 확인"""
		return self.get_status() == ReservationStatus.CANCELLED
