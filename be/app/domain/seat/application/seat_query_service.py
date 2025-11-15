from typing import Optional

from app.domain.seat.application.ports.inbound.seat_query_use_case import SeatQueryUseCase
from app.domain.seat.application.ports.outbound.seat_repository import SeatRepository
from app.domain.seat.domain.seat import Seat


class SeatQueryService(SeatQueryUseCase):

	def __init__(self, seat_repository: SeatRepository):
		self.seat_repository = seat_repository

	async def get_seat_by_id(self, seat_id: int) -> Optional[Seat]:
		return await self.seat_repository.find_by_id(seat_id)

	async def get_seat_list_all(self) -> list[Seat]:
		return await self.seat_repository.find_all()
