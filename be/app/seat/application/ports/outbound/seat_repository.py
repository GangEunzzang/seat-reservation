from abc import ABC, abstractmethod
from typing import Optional

from app.seat.domain.seat import Seat


class SeatRepository(ABC):
	@abstractmethod
	async def save(self, seat: Seat) -> Seat:
		pass

	@abstractmethod
	async def find_by_id(self, seat_id: int) -> Optional[Seat]:
		pass

	@abstractmethod
	async def find_all(self) -> list[Seat]:
		pass

	@abstractmethod
	async def delete(self, seat_id: int) -> None:
		pass
