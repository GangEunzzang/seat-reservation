from abc import ABC, abstractmethod
from typing import Optional

from app.zone.domain.zone import Zone


class ZoneRepository(ABC):

	@abstractmethod
	async def save(self, zone: Zone) -> Zone:
		pass

	@abstractmethod
	async def find_by_id(self, zone_id: int) -> Optional[Zone]:
		pass

	@abstractmethod
	async def find_all_by_episode_id(self, episode_id: int) -> list[Zone]:
		pass

	@abstractmethod
	async def delete(self, zone_id: int) -> None:
		pass
