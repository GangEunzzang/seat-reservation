import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.table.adapter.outbound.persistence.sqlalchemy_table_repository import SQLAlchemyTableRepository
from app.table.application.table_query_service import TableQueryService
from test.domain.table.table_fixture import TableFixture


@pytest.fixture
def table_repository(async_session: AsyncSession) -> SQLAlchemyTableRepository:
	return SQLAlchemyTableRepository(async_session)


@pytest.fixture
def table_query_service(table_repository) -> TableQueryService:
	return TableQueryService(table_repository)


@pytest.mark.asyncio
async def test_get_table_by_id(table_query_service, table_repository):
	# Given
	table = TableFixture.create_table(episode_id=1)
	saved_table = await table_repository.save(table)

	# When
	result = await table_query_service.get_table_by_id(saved_table.id)

	# Then
	assert result is not None
	assert result.id == saved_table.id
	assert result.episode_id == 1


@pytest.mark.asyncio
async def test_get_table_by_id_not_found(table_query_service):
	# Given
	NON_EXISTENT_TABLE_ID = 9999

	# When
	result = await table_query_service.get_table_by_id(NON_EXISTENT_TABLE_ID)

	# Then
	assert result is None


@pytest.mark.asyncio
async def test_get_table_list_all(table_query_service, table_repository):
	# Given
	tables = TableFixture.create_multiple_tables(episode_id=1, count=3)
	for table in tables:
		await table_repository.save(table)

	# When
	result = await table_query_service.get_table_list_all()

	# Then
	assert len(result) == 3


@pytest.mark.asyncio
async def test_get_table_list_all_empty(table_query_service):
	# When
	result = await table_query_service.get_table_list_all()

	# Then
	assert result == []
