from app.seat.application.ports.inbound.seat_query_use_case import SeatQueryUseCase
from app.seat.application.ports.outbound.seat_repository import SeatRepository
from app.seat.domain.seat import Seat
from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode


class SeatQueryService(SeatQueryUseCase):

	def __init__(self, seat_repository: SeatRepository):
		self.seat_repository = seat_repository

	async def get_seat_by_id(self, seat_id: int) -> Seat:
		seat = await self.seat_repository.find_by_id(seat_id)
		if not seat:
			raise DomainException(ErrorCode.SEAT_NOT_FOUND)
		return seat

	async def get_seat_list_all(self) -> list[Seat]:
		return await self.seat_repository.find_all()
