from abc import ABC, abstractmethod
from typing import Optional

from app.episode.domain.episode import Episode


class EpisodeRepository(ABC):
	@abstractmethod
	async def save(self, episode: Episode) -> Episode:
		pass

	@abstractmethod
	async def find_by_id(self, episode_id: int) -> Optional[Episode]:
		pass

	@abstractmethod
	async def find_all(self) -> list[Episode]:
		pass

	@abstractmethod
	async def delete(self, episode_id: int) -> None:
		pass
