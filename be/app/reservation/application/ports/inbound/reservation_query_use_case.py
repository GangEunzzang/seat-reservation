from abc import ABC, abstractmethod

from app.reservation.domain.reservation import Reservation


class ReservationQueryUseCase(ABC):

	@abstractmethod
	async def get_reservation_by_id(self, reservation_id: int) -> Reservation:
		"""ID로 예약 조회"""
		pass

	@abstractmethod
	async def get_reservation_list_all(self) -> list[Reservation]:
		"""전체 예약 목록 조회"""
		pass
