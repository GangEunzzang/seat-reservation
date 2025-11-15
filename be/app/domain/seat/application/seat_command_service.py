from app.core.exceptions import DomainException, ErrorCode
from app.domain.seat.application.ports.inbound.seat_command_use_case import SeatCommandUseCase
from app.domain.seat.application.ports.outbound.seat_repository import SeatRepository
from app.domain.seat.domain.seat import Seat


class SeatCommandService(SeatCommandUseCase):

	def __init__(self, seat_repository: SeatRepository):
		self.seat_repository = seat_repository

	async def create(self, table_id: int, seat_number: int) -> Seat:
		seat = Seat.create(table_id=table_id, seat_number=seat_number)
		return await self.seat_repository.save(seat)

	async def delete(self, seat_id: int) -> None:
		seat = await self.seat_repository.find_by_id(seat_id)
		if not seat:
			raise DomainException(ErrorCode.SEAT_NOT_FOUND)

		await self.seat_repository.delete(seat_id)
