from app.reservation.application.ports.inbound.reservation_query_use_case import ReservationQueryUseCase
from app.reservation.application.ports.outbound.reservation_repository import ReservationRepository
from app.reservation.domain.reservation import Reservation
from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode


class ReservationQueryService(ReservationQueryUseCase):

	def __init__(self, reservation_repository: ReservationRepository):
		self.reservation_repository = reservation_repository

	async def get_reservation_by_id(self, reservation_id: int) -> Reservation:
		reservation = await self.reservation_repository.find_by_id(reservation_id)
		if not reservation:
			raise DomainException(ErrorCode.RESERVATION_NOT_FOUND)
		return reservation

	async def get_reservation_list_all(self) -> list[Reservation]:
		return await self.reservation_repository.find_all()
