from abc import ABC, abstractmethod
from typing import Optional

from app.domain.reservation.domain.reservation import Reservation


class ReservationRepository(ABC):
	@abstractmethod
	async def save(self, reservation: Reservation) -> Reservation:
		pass

	@abstractmethod
	async def find_by_id(self, reservation_id: int) -> Optional[Reservation]:
		pass

	@abstractmethod
	async def find_all(self) -> list[Reservation]:
		pass

	@abstractmethod
	async def delete(self, reservation_id: int) -> None:
		pass
