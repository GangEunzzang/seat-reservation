from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.seat.application.ports.outbound.seat_repository import SeatRepository
from app.seat.domain.seat import Seat


class SQLAlchemySeatRepository(SeatRepository):
	def __init__(self, session: AsyncSession):
		self.session = session

	async def save(self, seat: Seat) -> Seat:
		self.session.add(seat)
		await self.session.flush()
		await self.session.refresh(seat)
		return seat

	async def find_by_id(self, seat_id: int) -> Optional[Seat]:
		return await self.session.get(Seat, seat_id)

	async def find_all(self) -> list[Seat]:
		stmt = select(Seat)
		result = await self.session.execute(stmt)
		return list(result.scalars().all())

	async def delete(self, seat_id: int) -> None:
		stmt = delete(Seat).where(Seat.id == seat_id)
		await self.session.execute(stmt)
		await self.session.flush()
