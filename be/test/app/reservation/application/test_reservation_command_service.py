import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode
from app.reservation.adapter.outbound.persistence.sqlalchemy_reservation_repository import SQLAlchemyReservationRepository
from app.reservation.application.reservation_command_service import ReservationCommandService
from test.app.reservation.reservation_fixture import ReservationFixture


@pytest.fixture
def reservation_repository(async_session: AsyncSession) -> SQLAlchemyReservationRepository:
	return SQLAlchemyReservationRepository(async_session)


@pytest.fixture
def reservation_command_service(reservation_repository) -> ReservationCommandService:
	return ReservationCommandService(reservation_repository)


@pytest.mark.asyncio
async def test_create_reservation(reservation_command_service):
	# Given
	user_id = 1
	seat_id = 1

	# When
	result = await reservation_command_service.create(user_id, seat_id)

	# Then
	assert result.id is not None
	assert result.user_id == user_id
	assert result.seat_id == seat_id
	assert result.is_active()


@pytest.mark.asyncio
async def test_create_reservation_seat_already_reserved(reservation_command_service, reservation_repository):
	# Given
	user_id = 1
	seat_id = 1
	existing_reservation = ReservationFixture.create_reservation(user_id=user_id, seat_id=seat_id)
	await reservation_repository.save(existing_reservation)

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await reservation_command_service.create(user_id=2, seat_id=seat_id)

	assert exc_info.value.error_code == ErrorCode.SEAT_ALREADY_RESERVED


@pytest.mark.asyncio
async def test_cancel_reservation(reservation_command_service, reservation_repository):
	# Given
	reservation = ReservationFixture.create_reservation(user_id=1, seat_id=1)
	saved_reservation = await reservation_repository.save(reservation)

	# When
	await reservation_command_service.cancel(saved_reservation.id)

	# Then
	found_reservation = await reservation_repository.find_by_id(saved_reservation.id)
	assert found_reservation is not None
	assert found_reservation.is_cancelled()
	assert found_reservation.cancelled_at is not None


@pytest.mark.asyncio
async def test_cancel_reservation_not_found(reservation_command_service):
	# Given
	NON_EXISTENT_RESERVATION_ID = 9999

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await reservation_command_service.cancel(NON_EXISTENT_RESERVATION_ID)

	assert exc_info.value.error_code == ErrorCode.RESERVATION_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_reservation(reservation_command_service, reservation_repository):
	# Given
	reservation = ReservationFixture.create_reservation(user_id=1, seat_id=1)
	saved_reservation = await reservation_repository.save(reservation)

	# When
	await reservation_command_service.delete(saved_reservation.id)

	# Then
	found_reservation = await reservation_repository.find_by_id(saved_reservation.id)
	assert found_reservation is None


@pytest.mark.asyncio
async def test_delete_reservation_not_found(reservation_command_service):
	# Given
	NON_EXISTENT_RESERVATION_ID = 9999

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await reservation_command_service.delete(NON_EXISTENT_RESERVATION_ID)

	assert exc_info.value.error_code == ErrorCode.RESERVATION_NOT_FOUND
