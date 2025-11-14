from abc import ABC, abstractmethod

from app.domain.table.domain.table import Table


class TableCommandUseCase(ABC):

	@abstractmethod
	async def create(self, episode_id: int) -> Table:
		"""테이블 생성"""
		pass

	@abstractmethod
	async def delete(self, table_id: int) -> None:
		"""테이블 삭제"""
		pass
