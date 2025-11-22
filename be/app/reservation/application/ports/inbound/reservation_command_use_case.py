from abc import ABC, abstractmethod

from app.reservation.domain.reservation import Reservation


class ReservationCommandUseCase(ABC):

	@abstractmethod
	async def create(self, user_id: int, seat_id: int, password: str) -> Reservation:
		"""예약 생성"""
		pass

	@abstractmethod
	async def cancel(self, reservation_id: int, password: str) -> None:
		"""예약 취소"""
		pass

	@abstractmethod
	async def delete(self, reservation_id: int) -> None:
		"""예약 삭제"""
		pass
