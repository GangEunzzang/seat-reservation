from core.exception.domain_exception import DomainException, ErrorCode
from app.table.application.ports.inbound.table_command_use_case import TableCommandUseCase
from app.table.application.ports.outbound.table_repository import TableRepository
from app.table.domain.table import Table


class TableCommandService(TableCommandUseCase):

	def __init__(self, table_repository: TableRepository):
		self.table_repository = table_repository

	async def create(self, episode_id: int, zone_id: int, x: int, y: int, name: str) -> Table:
		table = Table.create(episode_id=episode_id, zone_id=zone_id, x=x, y=y, name=name)
		return await self.table_repository.save(table)

	async def update_position(self, table_id: int, x: int, y: int) -> Table:
		table = await self.table_repository.find_by_id(table_id)
		if not table:
			raise DomainException(ErrorCode.TABLE_NOT_FOUND)

		table.update_position(x, y)
		return await self.table_repository.save(table)

	async def delete(self, table_id: int) -> None:
		table = await self.table_repository.find_by_id(table_id)
		if not table:
			raise DomainException(ErrorCode.TABLE_NOT_FOUND)

		await self.table_repository.delete(table_id)
