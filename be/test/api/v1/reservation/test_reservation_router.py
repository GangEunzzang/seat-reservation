"""Reservation Router Integration Tests"""
import pytest
import pytest_asyncio
from httpx import AsyncClient

from test.app.reservation.reservation_fixture import ReservationFixture


@pytest_asyncio.fixture
async def created_reservation(async_client: AsyncClient) -> dict:
	return await ReservationFixture.create_via_api(async_client)


@pytest.mark.asyncio
async def test_create_reservation_success(async_client: AsyncClient):
	request_data = ReservationFixture.create_request_dict()
	response = await async_client.post("/api/v1/reservation", json=request_data)
	assert response.status_code == 201
	data = response.json()["data"]
	assert data["user_id"] == 1
	assert data["seat_id"] == 1
	assert data["status"] == "reserve"
	assert data["cancelled_at"] is None
	assert "id" in data
	assert "reserved_at" in data


@pytest.mark.asyncio
async def test_get_reservation_success(async_client: AsyncClient, created_reservation: dict):
	reservation_id = created_reservation["id"]
	response = await async_client.get(f"/api/v1/reservation/{reservation_id}")
	assert response.status_code == 200
	assert response.json()["data"]["id"] == reservation_id


@pytest.mark.asyncio
async def test_get_reservation_not_found(async_client: AsyncClient):
	response = await async_client.get("/api/v1/reservation/9999")
	assert response.status_code == 404
	assert response.json()["code"] == "RESERVATION_NOT_FOUND"


@pytest.mark.asyncio
async def test_list_reservations_empty(async_client: AsyncClient):
	response = await async_client.get("/api/v1/reservation")
	assert response.status_code == 200
	assert response.json()["data"] == []


@pytest.mark.asyncio
async def test_list_reservations_with_data(async_client: AsyncClient):
	await ReservationFixture.create_multiple_via_api(async_client, [1, 2], [1, 2])
	response = await async_client.get("/api/v1/reservation")
	assert response.status_code == 200
	assert len(response.json()["data"]) == 2


@pytest.mark.asyncio
async def test_cancel_reservation_success(async_client: AsyncClient, created_reservation: dict):
	reservation_id = created_reservation["id"]
	response = await async_client.patch(f"/api/v1/reservation/{reservation_id}/cancel")
	assert response.status_code == 204
	get_response = await async_client.get(f"/api/v1/reservation/{reservation_id}")
	assert get_response.json()["data"]["status"] == "cancel"
	assert get_response.json()["data"]["cancelled_at"] is not None


@pytest.mark.asyncio
async def test_cancel_reservation_not_found(async_client: AsyncClient):
	response = await async_client.patch("/api/v1/reservation/9999/cancel")
	assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_reservation_success(async_client: AsyncClient, created_reservation: dict):
	reservation_id = created_reservation["id"]
	response = await async_client.delete(f"/api/v1/reservation/{reservation_id}")
	assert response.status_code == 204
	assert (await async_client.get(f"/api/v1/reservation/{reservation_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_reservation_not_found(async_client: AsyncClient):
	response = await async_client.delete("/api/v1/reservation/9999")
	assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_reservation_duplicate_seat(async_client: AsyncClient, created_reservation: dict):
	duplicate_request = ReservationFixture.create_request_dict(user_id=2, seat_id=1)
	response = await async_client.post("/api/v1/reservation", json=duplicate_request)
	assert response.status_code == 409
	assert response.json()["code"] == "SEAT_ALREADY_RESERVED"
