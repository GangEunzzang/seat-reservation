from typing import Optional

from app.domain.reservation.application.ports.inbound.reservation_query_use_case import ReservationQueryUseCase
from app.domain.reservation.application.ports.outbound.reservation_repository import ReservationRepository
from app.domain.reservation.domain.reservation import Reservation


class ReservationQueryService(ReservationQueryUseCase):

	def __init__(self, reservation_repository: ReservationRepository):
		self.reservation_repository = reservation_repository

	async def get_reservation_by_id(self, reservation_id: int) -> Optional[Reservation]:
		return await self.reservation_repository.find_by_id(reservation_id)

	async def get_reservation_list_all(self) -> list[Reservation]:
		return await self.reservation_repository.find_all()
