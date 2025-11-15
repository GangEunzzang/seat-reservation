import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.exception.domain_exception import DomainException, ErrorCode
from app.table.adapter.outbound.persistence.sqlalchemy_table_repository import SQLAlchemyTableRepository
from app.table.application.table_command_service import TableCommandService
from test.app.table.table_fixture import TableFixture


@pytest.fixture
def table_repository(async_session: AsyncSession) -> SQLAlchemyTableRepository:
	return SQLAlchemyTableRepository(async_session)


@pytest.fixture
def table_command_service(table_repository) -> TableCommandService:
	return TableCommandService(table_repository)


@pytest.mark.asyncio
async def test_create_table(table_command_service):
	# Given
	episode_id = 1

	# When
	result = await table_command_service.create(episode_id)

	# Then
	assert result.id is not None
	assert result.episode_id == episode_id


@pytest.mark.asyncio
async def test_delete_table(table_command_service, table_repository):
	# Given
	table = TableFixture.create_table(episode_id=1)
	saved_table = await table_repository.save(table)

	# When
	await table_command_service.delete(saved_table.id)

	# Then
	found_table = await table_repository.find_by_id(saved_table.id)
	assert found_table is None


@pytest.mark.asyncio
async def test_delete_table_not_found(table_command_service):
	# Given
	NON_EXISTENT_TABLE_ID = 9999

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await table_command_service.delete(NON_EXISTENT_TABLE_ID)

	assert exc_info.value.error_code == ErrorCode.TABLE_NOT_FOUND
