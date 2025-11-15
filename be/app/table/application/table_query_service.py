from typing import Optional

from app.table.application.ports.inbound.table_query_use_case import TableQueryUseCase
from app.table.application.ports.outbound.table_repository import TableRepository
from app.table.domain.table import Table


class TableQueryService(TableQueryUseCase):

	def __init__(self, table_repository: TableRepository):
		self.table_repository = table_repository

	async def get_table_by_id(self, table_id: int) -> Optional[Table]:
		return await self.table_repository.find_by_id(table_id)

	async def get_table_list_all(self) -> list[Table]:
		return await self.table_repository.find_all()
