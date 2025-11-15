from typing import Optional

from app.domain.episode.application.ports.inbound.episode_query_use_case import EpisodeQueryUseCase
from app.domain.episode.application.ports.outbound.episode_repository import EpisodeRepository
from app.domain.episode.domain.episode import Episode


class EpisodeQueryService(EpisodeQueryUseCase):

	def __init__(self, episode_repository: EpisodeRepository):
		self.episode_repository = episode_repository

	async def get_episode_by_id(self, episode_id: int) -> Optional[Episode]:
		return await self.episode_repository.find_by_id(episode_id)

	async def get_episode_list_all(self) -> list[Episode]:
		return await self.episode_repository.find_all()
