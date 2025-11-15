from abc import ABC, abstractmethod
from typing import Optional

from app.episode.domain.episode import Episode


class EpisodeQueryUseCase(ABC):

	@abstractmethod
	async def get_episode_by_id(self, episode_id: int) -> Optional[Episode]:
		"""ID로 에피소드 조회"""
		pass

	@abstractmethod
	async def get_episode_list_all(self) -> list[Episode]:
		"""전체 에피소드 목록 조회"""
		pass
