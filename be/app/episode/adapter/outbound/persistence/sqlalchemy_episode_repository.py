from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.episode.application.ports.outbound.episode_repository import EpisodeRepository
from app.episode.domain.episode import Episode


class SQLAlchemyEpisodeRepository(EpisodeRepository):
	def __init__(self, session: AsyncSession):
		self.session = session

	async def save(self, episode: Episode) -> Episode:
		self.session.add(episode)
		await self.session.flush()
		await self.session.refresh(episode)
		return episode

	async def find_by_id(self, episode_id: int) -> Optional[Episode]:
		return await self.session.get(Episode, episode_id)

	async def find_all(self) -> list[Episode]:
		stmt = select(Episode)
		result = await self.session.execute(stmt)
		return list(result.scalars().all())

	async def delete(self, episode_id: int) -> None:
		stmt = delete(Episode).where(Episode.id == episode_id)
		await self.session.execute(stmt)
		await self.session.flush()
