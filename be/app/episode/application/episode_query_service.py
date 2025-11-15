from app.episode.application.ports.inbound.episode_query_use_case import EpisodeQueryUseCase
from app.episode.application.ports.outbound.episode_repository import EpisodeRepository
from app.episode.domain.episode import Episode
from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode


class EpisodeQueryService(EpisodeQueryUseCase):

	def __init__(self, episode_repository: EpisodeRepository):
		self.episode_repository = episode_repository

	async def get_episode_by_id(self, episode_id: int) -> Episode:
		episode = await self.episode_repository.find_by_id(episode_id)
		if not episode:
			raise DomainException(ErrorCode.EPISODE_NOT_FOUND)
		return episode

	async def get_episode_list_all(self) -> list[Episode]:
		return await self.episode_repository.find_all()
