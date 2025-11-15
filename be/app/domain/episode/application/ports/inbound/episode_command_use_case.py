from abc import ABC, abstractmethod
from datetime import date

from app.domain.episode.domain.episode import Episode


class EpisodeCommandUseCase(ABC):

	@abstractmethod
	async def create(self, year: int, name: str, start_date: date, end_date: date) -> Episode:
		"""에피소드 생성"""
		pass

	@abstractmethod
	async def delete(self, episode_id: int) -> None:
		"""에피소드 삭제"""
		pass
