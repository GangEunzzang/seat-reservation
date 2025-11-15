from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.reservation.application.ports.outbound.reservation_repository import ReservationRepository
from app.reservation.domain.reservation import Reservation


class SQLAlchemyReservationRepository(ReservationRepository):
	def __init__(self, session: AsyncSession):
		self.session = session

	async def save(self, reservation: Reservation) -> Reservation:
		self.session.add(reservation)
		await self.session.flush()
		await self.session.refresh(reservation)
		return reservation

	async def find_by_id(self, reservation_id: int) -> Optional[Reservation]:
		return await self.session.get(Reservation, reservation_id)

	async def find_all(self) -> list[Reservation]:
		stmt = select(Reservation)
		result = await self.session.execute(stmt)
		return list(result.scalars().all())

	async def delete(self, reservation_id: int) -> None:
		stmt = delete(Reservation).where(Reservation.id == reservation_id)
		await self.session.execute(stmt)
		await self.session.flush()

	async def find_active_by_seat_id(self, seat_id: int) -> Optional[Reservation]:
		from app.reservation.domain.reservation_status import ReservationStatus
		stmt = (
		select(Reservation)
		.where(
			Reservation.seat_id == seat_id,
			Reservation.status == ReservationStatus.RESERVED.code
		))
		result = await self.session.execute(stmt)
		return result.scalars().first()
