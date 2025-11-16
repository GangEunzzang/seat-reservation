"""Seat Router Integration Tests"""
import pytest
import pytest_asyncio
from httpx import AsyncClient

from test.app.seat.seat_fixture import SeatFixture


@pytest_asyncio.fixture
async def created_seat(async_client: AsyncClient) -> dict:
	return await SeatFixture.create_via_api(async_client)


@pytest.mark.asyncio
async def test_create_seat_success(async_client: AsyncClient):
	request_data = SeatFixture.create_request_dict()
	response = await async_client.post("/api/v1/seat", json=request_data)
	assert response.status_code == 201
	assert response.json()["data"]["table_id"] == 1
	assert response.json()["data"]["seat_number"] == 1
	assert "id" in response.json()["data"]


@pytest.mark.asyncio
async def test_get_seat_success(async_client: AsyncClient, created_seat: dict):
	seat_id = created_seat["id"]
	response = await async_client.get(f"/api/v1/seat/{seat_id}")
	assert response.status_code == 200
	assert response.json()["data"]["id"] == seat_id


@pytest.mark.asyncio
async def test_get_seat_not_found(async_client: AsyncClient):
	response = await async_client.get("/api/v1/seat/9999")
	assert response.status_code == 404
	assert response.json()["code"] == "SEAT_NOT_FOUND"


@pytest.mark.asyncio
async def test_list_seats_empty(async_client: AsyncClient):
	response = await async_client.get("/api/v1/seat")
	assert response.status_code == 200
	assert response.json()["data"] == []


@pytest.mark.asyncio
async def test_list_seats_with_data(async_client: AsyncClient):
	await SeatFixture.create_multiple_via_api(async_client, count=3)
	response = await async_client.get("/api/v1/seat")
	assert response.status_code == 200
	assert len(response.json()["data"]) == 3


@pytest.mark.asyncio
async def test_delete_seat_success(async_client: AsyncClient, created_seat: dict):
	seat_id = created_seat["id"]
	response = await async_client.delete(f"/api/v1/seat/{seat_id}")
	assert response.status_code == 204
	assert (await async_client.get(f"/api/v1/seat/{seat_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_seat_not_found(async_client: AsyncClient):
	response = await async_client.delete("/api/v1/seat/9999")
	assert response.status_code == 404
