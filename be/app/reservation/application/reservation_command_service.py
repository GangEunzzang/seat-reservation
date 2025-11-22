from core.exception.domain_exception import DomainException, ErrorCode
from app.reservation.application.ports.inbound.reservation_command_use_case import ReservationCommandUseCase
from app.reservation.application.ports.outbound.reservation_repository import ReservationRepository
from app.reservation.domain.reservation import Reservation


class ReservationCommandService(ReservationCommandUseCase):

	def __init__(self, reservation_repository: ReservationRepository):
		self.reservation_repository = reservation_repository

	async def create(self, user_id: int, seat_id: int, password: str) -> Reservation:
		# 좌석이 이미 예약되어 있는지 확인
		existing_reservation = await self.reservation_repository.find_active_by_seat_id(seat_id)
		if existing_reservation:
			raise DomainException(ErrorCode.SEAT_ALREADY_RESERVED)

		reservation = Reservation.create(user_id=user_id, seat_id=seat_id, password=password)
		return await self.reservation_repository.save(reservation)

	async def cancel(self, reservation_id: int, password: str) -> None:
		reservation = await self.reservation_repository.find_by_id(reservation_id)
		if not reservation:
			raise DomainException(ErrorCode.RESERVATION_NOT_FOUND)

		if not reservation.verify_password(password):
			raise DomainException(ErrorCode.INVALID_RESERVATION_PASSWORD)

		reservation.cancel()
		await self.reservation_repository.save(reservation)

	async def delete(self, reservation_id: int) -> None:
		reservation = await self.reservation_repository.find_by_id(reservation_id)
		if not reservation:
			raise DomainException(ErrorCode.RESERVATION_NOT_FOUND)

		await self.reservation_repository.delete(reservation_id)
