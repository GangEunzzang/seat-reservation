import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.reservation.adapter.outbound.persistence.sqlalchemy_reservation_repository import SQLAlchemyReservationRepository
from app.reservation.application.reservation_query_service import ReservationQueryService
from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode
from test.app.reservation.reservation_fixture import ReservationFixture


@pytest.fixture
def reservation_repository(async_session: AsyncSession) -> SQLAlchemyReservationRepository:
	return SQLAlchemyReservationRepository(async_session)


@pytest.fixture
def reservation_query_service(reservation_repository) -> ReservationQueryService:
	return ReservationQueryService(reservation_repository)


@pytest.mark.asyncio
async def test_get_reservation_by_id(reservation_query_service, reservation_repository):
	# Given
	reservation = ReservationFixture.create_reservation(user_id=1, seat_id=1)
	saved_reservation = await reservation_repository.save(reservation)

	# When
	result = await reservation_query_service.get_reservation_by_id(saved_reservation.id)

	# Then
	assert result is not None
	assert result.id == saved_reservation.id
	assert result.user_id == 1
	assert result.seat_id == 1


@pytest.mark.asyncio
async def test_get_reservation_by_id_not_found(reservation_query_service):
	# Given
	NON_EXISTENT_RESERVATION_ID = 9999

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await reservation_query_service.get_reservation_by_id(NON_EXISTENT_RESERVATION_ID)

	assert exc_info.value.error_code == ErrorCode.RESERVATION_NOT_FOUND


@pytest.mark.asyncio
async def test_get_reservation_list_all(reservation_query_service, reservation_repository):
	# Given
	reservations = ReservationFixture.create_multiple_reservations(
		user_ids=[1, 2, 3],
		seat_ids=[1, 2, 3]
	)
	for reservation in reservations:
		await reservation_repository.save(reservation)

	# When
	result = await reservation_query_service.get_reservation_list_all()

	# Then
	assert len(result) == 3


@pytest.mark.asyncio
async def test_get_reservation_list_all_empty(reservation_query_service):
	# When
	result = await reservation_query_service.get_reservation_list_all()

	# Then
	assert result == []
