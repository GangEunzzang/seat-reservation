import pytest
from unittest.mock import AsyncMock

from app.domain.table.application.table_command_service import TableCommandService
from test.domain.table.table_fixture import TableFixture


@pytest.fixture
def mock_table_repository():
	return AsyncMock()


@pytest.fixture
def table_command_service(mock_table_repository):
	return TableCommandService(mock_table_repository)


@pytest.mark.asyncio
async def test_create_table(table_command_service, mock_table_repository):
	# Given
	episode_id = 1
	created_table = TableFixture.create_table(episode_id=episode_id)
	created_table.id = 1
	mock_table_repository.save.return_value = created_table

	# When
	result = await table_command_service.create(episode_id)

	# Then
	assert result.id == 1
	assert result.episode_id == 1
	mock_table_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_delete_table(table_command_service, mock_table_repository):
	# Given
	table_id = 1
	existing_table = TableFixture.create_table(episode_id=1)
	existing_table.id = table_id
	mock_table_repository.find_by_id.return_value = existing_table

	# When
	await table_command_service.delete(table_id)

	# Then
	mock_table_repository.find_by_id.assert_called_once_with(table_id)
	mock_table_repository.delete.assert_called_once_with(table_id)


@pytest.mark.asyncio
async def test_delete_table_not_found(table_command_service, mock_table_repository):
	# Given
	table_id = 9999
	mock_table_repository.find_by_id.return_value = None

	# When & Then
	with pytest.raises(ValueError) as exc_info:
		await table_command_service.delete(table_id)

	assert "not found" in str(exc_info.value)
	mock_table_repository.find_by_id.assert_called_once_with(table_id)
	mock_table_repository.delete.assert_not_called()
