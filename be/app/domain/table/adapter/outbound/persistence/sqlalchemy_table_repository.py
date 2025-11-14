from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.table.application.ports.outbound.table_repository import TableRepository
from app.domain.table.domain.table import Table


class SQLAlchemyTableRepository(TableRepository):
	def __init__(self, session: AsyncSession):
		self.session = session

	async def save(self, table: Table) -> Table:
		self.session.add(table)
		await self.session.flush()
		await self.session.refresh(table)
		return table

	async def find_by_id(self, table_id: int) -> Optional[Table]:
		return await self.session.get(Table, table_id)

	async def find_all(self) -> list[Table]:
		stmt = select(Table)
		result = await self.session.execute(stmt)
		return list(result.scalars().all())

	async def delete(self, table_id: int) -> None:
		stmt = delete(Table).where(Table.id == table_id)
		await self.session.execute(stmt)
		await self.session.flush()
