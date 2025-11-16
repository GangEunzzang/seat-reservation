"""Table Router Integration Tests"""
import pytest
import pytest_asyncio
from httpx import AsyncClient

from test.app.table.table_fixture import TableFixture


@pytest_asyncio.fixture
async def created_table(async_client: AsyncClient) -> dict:
	return await TableFixture.create_via_api(async_client)


@pytest.mark.asyncio
async def test_create_table_success(async_client: AsyncClient):
	request_data = TableFixture.create_request_dict()
	response = await async_client.post("/api/v1/table", json=request_data)
	assert response.status_code == 201
	assert response.json()["data"]["episode_id"] == 1
	assert "id" in response.json()["data"]


@pytest.mark.asyncio
async def test_get_table_success(async_client: AsyncClient, created_table: dict):
	table_id = created_table["id"]
	response = await async_client.get(f"/api/v1/table/{table_id}")
	assert response.status_code == 200
	assert response.json()["data"]["id"] == table_id


@pytest.mark.asyncio
async def test_get_table_not_found(async_client: AsyncClient):
	response = await async_client.get("/api/v1/table/9999")
	assert response.status_code == 404
	assert response.json()["code"] == "TABLE_NOT_FOUND"


@pytest.mark.asyncio
async def test_list_tables_empty(async_client: AsyncClient):
	response = await async_client.get("/api/v1/table")
	assert response.status_code == 200
	assert response.json()["data"] == []


@pytest.mark.asyncio
async def test_list_tables_with_data(async_client: AsyncClient):
	await TableFixture.create_multiple_via_api(async_client, count=3)
	response = await async_client.get("/api/v1/table")
	assert response.status_code == 200
	assert len(response.json()["data"]) == 3


@pytest.mark.asyncio
async def test_delete_table_success(async_client: AsyncClient, created_table: dict):
	table_id = created_table["id"]
	response = await async_client.delete(f"/api/v1/table/{table_id}")
	assert response.status_code == 204
	assert (await async_client.get(f"/api/v1/table/{table_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_table_not_found(async_client: AsyncClient):
	response = await async_client.delete("/api/v1/table/9999")
	assert response.status_code == 404
