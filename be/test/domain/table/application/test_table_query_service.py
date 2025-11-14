import pytest
from unittest.mock import AsyncMock

from app.domain.table.application.table_query_service import TableQueryService
from test.domain.table.table_fixture import TableFixture


@pytest.fixture
def mock_table_repository():
	return AsyncMock()


@pytest.fixture
def table_query_service(mock_table_repository):
	return TableQueryService(mock_table_repository)


@pytest.mark.asyncio
async def test_get_table_by_id(table_query_service, mock_table_repository):
	# Given
	table_id = 1
	expected_table = TableFixture.create_table(episode_id=1)
	expected_table.id = table_id
	mock_table_repository.find_by_id.return_value = expected_table

	# When
	result = await table_query_service.get_table_by_id(table_id)

	# Then
	assert result is not None
	assert result.id == table_id
	assert result.episode_id == 1
	mock_table_repository.find_by_id.assert_called_once_with(table_id)


@pytest.mark.asyncio
async def test_get_table_by_id_not_found(table_query_service, mock_table_repository):
	# Given
	table_id = 9999
	mock_table_repository.find_by_id.return_value = None

	# When
	result = await table_query_service.get_table_by_id(table_id)

	# Then
	assert result is None
	mock_table_repository.find_by_id.assert_called_once_with(table_id)


@pytest.mark.asyncio
async def test_get_table_list_all(table_query_service, mock_table_repository):
	# Given
	table1 = TableFixture.create_table(episode_id=1)
	table1.id = 1
	table2 = TableFixture.create_table(episode_id=1)
	table2.id = 2
	table3 = TableFixture.create_table(episode_id=2)
	table3.id = 3
	mock_table_repository.find_all.return_value = [table1, table2, table3]

	# When
	result = await table_query_service.get_table_list_all()

	# Then
	assert len(result) == 3
	assert result[0].id == 1
	assert result[1].id == 2
	assert result[2].id == 3
	mock_table_repository.find_all.assert_called_once()


@pytest.mark.asyncio
async def test_get_table_list_all_empty(table_query_service, mock_table_repository):
	# Given
	mock_table_repository.find_all.return_value = []

	# When
	result = await table_query_service.get_table_list_all()

	# Then
	assert len(result) == 0
	mock_table_repository.find_all.assert_called_once()
