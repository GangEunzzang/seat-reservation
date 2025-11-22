from abc import ABC, abstractmethod

from app.zone.domain.zone import Zone


class ZoneCommandUseCase(ABC):

	@abstractmethod
	async def create(self, episode_id: int, code: str, name: str) -> Zone:
		"""Zone 생성"""
		pass

	@abstractmethod
	async def update_name(self, zone_id: int, name: str) -> Zone:
		"""Zone 이름 수정"""
		pass

	@abstractmethod
	async def delete(self, zone_id: int) -> None:
		"""Zone 삭제"""
		pass
