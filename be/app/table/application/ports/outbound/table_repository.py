from abc import ABC, abstractmethod
from typing import Optional

from app.table.domain.table import Table


class TableRepository(ABC):
	@abstractmethod
	async def save(self, table: Table) -> Table:
		pass

	@abstractmethod
	async def find_by_id(self, table_id: int) -> Optional[Table]:
		pass

	@abstractmethod
	async def find_all(self) -> list[Table]:
		pass

	@abstractmethod
	async def delete(self, table_id: int) -> None:
		pass
