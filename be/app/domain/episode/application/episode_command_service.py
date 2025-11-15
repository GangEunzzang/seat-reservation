from datetime import date

from app.core.exceptions import DomainException, ErrorCode
from app.domain.episode.application.ports.inbound.episode_command_use_case import EpisodeCommandUseCase
from app.domain.episode.application.ports.outbound.episode_repository import EpisodeRepository
from app.domain.episode.domain.episode import Episode


class EpisodeCommandService(EpisodeCommandUseCase):

	def __init__(self, episode_repository: EpisodeRepository):
		self.episode_repository = episode_repository

	async def create(self, year: int, name: str, start_date: date, end_date: date) -> Episode:
		episode = Episode.create(year=year, name=name, start_date=start_date, end_date=end_date)
		return await self.episode_repository.save(episode)

	async def delete(self, episode_id: int) -> None:
		episode = await self.episode_repository.find_by_id(episode_id)
		if not episode:
			raise DomainException(ErrorCode.EPISODE_NOT_FOUND)

		await self.episode_repository.delete(episode_id)
