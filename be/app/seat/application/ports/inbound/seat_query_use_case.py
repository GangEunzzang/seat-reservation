from abc import ABC, abstractmethod

from app.seat.domain.seat import Seat


class SeatQueryUseCase(ABC):

	@abstractmethod
	async def get_seat_by_id(self, seat_id: int) -> Seat:
		"""ID로 좌석 조회"""
		pass

	@abstractmethod
	async def get_seat_list_all(self) -> list[Seat]:
		"""전체 좌석 목록 조회"""
		pass
