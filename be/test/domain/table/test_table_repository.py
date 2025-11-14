import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.table.adapter.outbound.persistence.sqlalchemy_table_repository import SQLAlchemyTableRepository
from test.domain.table.table_fixture import TableFixture


@pytest.fixture
def table_repository(async_session: AsyncSession) -> SQLAlchemyTableRepository:
	return SQLAlchemyTableRepository(async_session)


@pytest.mark.asyncio
async def test_save_table(table_repository):
	table = TableFixture.create_table(episode_id=1)
	saved_table = await table_repository.save(table)
	assert saved_table.id is not None
	assert saved_table.episode_id == 1


@pytest.mark.asyncio
async def test_find_by_id(table_repository):
	table = TableFixture.create_table(episode_id=2)
	saved_table = await table_repository.save(table)
	found_table = await table_repository.find_by_id(saved_table.id)
	assert found_table is not None
	assert found_table.id == saved_table.id
	assert found_table.episode_id == 2


@pytest.mark.asyncio
async def test_find_by_id_not_found(table_repository):
	found_table = await table_repository.find_by_id(9999)
	assert found_table is None


@pytest.mark.asyncio
async def test_find_all(table_repository):
	tables = TableFixture.create_multiple_tables(episode_id=1, count=3)
	for table in tables:
		await table_repository.save(table)
	all_tables = await table_repository.find_all()
	assert len(all_tables) == 3


@pytest.mark.asyncio
async def test_delete(table_repository):
	table = TableFixture.create_table(episode_id=3)
	saved_table = await table_repository.save(table)
	await table_repository.delete(saved_table.id)
	found_table = await table_repository.find_by_id(saved_table.id)
	assert found_table is None
