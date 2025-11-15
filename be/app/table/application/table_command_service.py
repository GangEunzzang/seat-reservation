from core.exception.domain_exception import DomainException, ErrorCode
from app.table.application.ports.inbound.table_command_use_case import TableCommandUseCase
from app.table.application.ports.outbound.table_repository import TableRepository
from app.table.domain.table import Table


class TableCommandService(TableCommandUseCase):

	def __init__(self, table_repository: TableRepository):
		self.table_repository = table_repository

	async def create(self, episode_id: int) -> Table:
		table = Table.create(episode_id=episode_id)
		return await self.table_repository.save(table)

	async def delete(self, table_id: int) -> None:
		table = await self.table_repository.find_by_id(table_id)
		if not table:
			raise DomainException(ErrorCode.TABLE_NOT_FOUND)

		await self.table_repository.delete(table_id)
