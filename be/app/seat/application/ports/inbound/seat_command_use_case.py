from abc import ABC, abstractmethod

from app.seat.domain.seat import Seat


class SeatCommandUseCase(ABC):

	@abstractmethod
	async def create(self, table_id: int, seat_number: int) -> Seat:
		"""좌석 생성"""
		pass

	@abstractmethod
	async def delete(self, seat_id: int) -> None:
		"""좌석 삭제"""
		pass
