"""User Router Integration Tests"""
import pytest
import pytest_asyncio
from httpx import AsyncClient

from test.app.user.user_fixture import UserFixture


@pytest_asyncio.fixture
async def created_user(async_client: AsyncClient) -> dict:
	return await UserFixture.create_via_api(async_client)


@pytest.mark.asyncio
async def test_register_user_success(async_client: AsyncClient):
	request_data = UserFixture.create_request_dict()
	response = await async_client.post("/api/v1/user", json=request_data)
	assert response.status_code == 201
	data = response.json()
	assert data["code"] == "200"
	assert "id" in data["data"]


@pytest.mark.asyncio
async def test_get_user_success(async_client: AsyncClient, created_user: dict):
	user_id = created_user["id"]
	response = await async_client.get(f"/api/v1/user/{user_id}")
	assert response.status_code == 200
	assert response.json()["data"]["id"] == user_id


@pytest.mark.asyncio
async def test_get_user_not_found(async_client: AsyncClient):
	response = await async_client.get("/api/v1/user/9999")
	assert response.status_code == 404
	assert response.json()["code"] == "USER_NOT_FOUND"


@pytest.mark.asyncio
async def test_list_users_empty(async_client: AsyncClient):
	response = await async_client.get("/api/v1/user")
	assert response.status_code == 200
	assert response.json()["data"] == []


@pytest.mark.asyncio
async def test_list_users_with_data(async_client: AsyncClient):
	await UserFixture.create_multiple_via_api(async_client, count=2)
	response = await async_client.get("/api/v1/user")
	assert response.status_code == 200
	assert len(response.json()["data"]) == 2


@pytest.mark.asyncio
async def test_delete_user_success(async_client: AsyncClient, created_user: dict):
	user_id = created_user["id"]
	response = await async_client.delete(f"/api/v1/user/{user_id}")
	assert response.status_code == 204
	assert (await async_client.get(f"/api/v1/user/{user_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_user_not_found(async_client: AsyncClient):
	response = await async_client.delete("/api/v1/user/9999")
	assert response.status_code == 404


@pytest.mark.asyncio
async def test_register_users_bulk_success(async_client: AsyncClient):
	request_data = [
		UserFixture.create_request_dict(name="홍길동", department="개발팀"),
		UserFixture.create_request_dict(name="김철수", department="기획팀"),
		UserFixture.create_request_dict(name="이영희", department="디자인팀")
	]
	response = await async_client.post("/api/v1/user/bulk", json=request_data)
	assert response.status_code == 201
	data = response.json()
	assert data["code"] == "200"
	assert len(data["data"]) == 3
	assert data["data"][0]["name"] == "홍길동"
	assert data["data"][1]["name"] == "김철수"
	assert data["data"][2]["name"] == "이영희"


@pytest.mark.asyncio
async def test_register_users_bulk_empty_list(async_client: AsyncClient):
	response = await async_client.post("/api/v1/user/bulk", json=[])
	assert response.status_code == 201
	data = response.json()
	assert data["code"] == "200"
	assert len(data["data"]) == 0
