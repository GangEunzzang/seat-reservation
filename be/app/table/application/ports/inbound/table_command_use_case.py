from abc import ABC, abstractmethod

from app.table.domain.table import Table


class TableCommandUseCase(ABC):

	@abstractmethod
	async def create(self, episode_id: int, zone_id: int, x: int, y: int, name: str) -> Table:
		"""테이블 생성"""
		pass

	@abstractmethod
	async def update_position(self, table_id: int, x: int, y: int) -> Table:
		"""테이블 위치 수정"""
		pass

	@abstractmethod
	async def delete(self, table_id: int) -> None:
		"""테이블 삭제"""
		pass
