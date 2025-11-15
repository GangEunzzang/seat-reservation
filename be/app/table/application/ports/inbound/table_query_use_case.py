from abc import ABC, abstractmethod

from app.table.domain.table import Table


class TableQueryUseCase(ABC):

	@abstractmethod
	async def get_table_by_id(self, table_id: int) -> Table:
		"""ID로 테이블 조회"""
		pass

	@abstractmethod
	async def get_table_list_all(self) -> list[Table]:
		"""전체 테이블 목록 조회"""
		pass
