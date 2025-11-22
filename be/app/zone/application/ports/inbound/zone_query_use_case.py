from abc import ABC, abstractmethod

from app.zone.domain.zone import Zone


class ZoneQueryUseCase(ABC):

	@abstractmethod
	async def get_zone_by_id(self, zone_id: int) -> Zone:
		"""Zone 조회"""
		pass

	@abstractmethod
	async def get_zones_by_episode_id(self, episode_id: int) -> list[Zone]:
		"""Episode별 Zone 목록 조회"""
		pass
