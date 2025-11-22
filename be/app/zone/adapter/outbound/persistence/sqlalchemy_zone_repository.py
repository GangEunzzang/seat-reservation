from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.zone.application.ports.outbound.zone_repository import ZoneRepository
from app.zone.domain.zone import Zone


class SQLAlchemyZoneRepository(ZoneRepository):

	def __init__(self, session: AsyncSession):
		self.session = session

	async def save(self, zone: Zone) -> Zone:
		self.session.add(zone)
		await self.session.flush()
		await self.session.refresh(zone)
		return zone

	async def find_by_id(self, zone_id: int) -> Optional[Zone]:
		return await self.session.get(Zone, zone_id)

	async def find_all_by_episode_id(self, episode_id: int) -> list[Zone]:
		stmt = select(Zone).where(Zone.episode_id == episode_id).order_by(Zone.code)
		result = await self.session.execute(stmt)
		return list(result.scalars().all())

	async def delete(self, zone_id: int) -> None:
		stmt = delete(Zone).where(Zone.id == zone_id)
		await self.session.execute(stmt)
		await self.session.flush()
