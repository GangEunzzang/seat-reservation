"""Episode Router Integration Tests"""
import pytest
import pytest_asyncio
from httpx import AsyncClient

from test.app.episode.episode_fixture import EpisodeFixture


@pytest_asyncio.fixture
async def created_episode(async_client: AsyncClient) -> dict:
	return await EpisodeFixture.create_via_api(async_client)


@pytest.mark.asyncio
async def test_create_episode_success(async_client: AsyncClient):
	request_data = EpisodeFixture.create_request_dict()
	response = await async_client.post("/api/v1/episode", json=request_data)
	assert response.status_code == 201
	data = response.json()["data"]
	assert data["year"] == 2024
	assert data["name"] == "2024 연간 총회"
	assert data["start_date"] == "2024-01-01"
	assert data["end_date"] == "2024-12-31"
	assert "id" in data


@pytest.mark.asyncio
async def test_get_episode_success(async_client: AsyncClient, created_episode: dict):
	episode_id = created_episode["id"]
	response = await async_client.get(f"/api/v1/episode/{episode_id}")
	assert response.status_code == 200
	assert response.json()["data"]["id"] == episode_id


@pytest.mark.asyncio
async def test_get_episode_not_found(async_client: AsyncClient):
	response = await async_client.get("/api/v1/episode/9999")
	assert response.status_code == 404
	assert response.json()["code"] == "EPISODE_NOT_FOUND"


@pytest.mark.asyncio
async def test_list_episodes_empty(async_client: AsyncClient):
	response = await async_client.get("/api/v1/episode")
	assert response.status_code == 200
	assert response.json()["data"] == []


@pytest.mark.asyncio
async def test_list_episodes_with_data(async_client: AsyncClient):
	await EpisodeFixture.create_multiple_via_api(async_client, years=[2022, 2023])
	response = await async_client.get("/api/v1/episode")
	assert response.status_code == 200
	assert len(response.json()["data"]) == 2


@pytest.mark.asyncio
async def test_delete_episode_success(async_client: AsyncClient, created_episode: dict):
	episode_id = created_episode["id"]
	response = await async_client.delete(f"/api/v1/episode/{episode_id}")
	assert response.status_code == 204
	assert (await async_client.get(f"/api/v1/episode/{episode_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_episode_not_found(async_client: AsyncClient):
	response = await async_client.delete("/api/v1/episode/9999")
	assert response.status_code == 404
