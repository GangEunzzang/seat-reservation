import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception.domain_exception import DomainException, ErrorCode
from app.domain.user.adapter.outbound.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.domain.user.application.user_command_service import UserCommandService
from app.domain.user.domain.user_register_request import UserRegisterRequest
from test.domain.user.user_fixture import UserFixture


@pytest.fixture
def user_repository(async_session: AsyncSession) -> SQLAlchemyUserRepository:
	return SQLAlchemyUserRepository(async_session)


@pytest.fixture
def user_command_service(user_repository) -> UserCommandService:
	return UserCommandService(user_repository)


@pytest.mark.asyncio
async def test_register_user(user_command_service):
	# Given
	request = UserRegisterRequest(
		user_code="TEST001",
		name="홍길동",
		department="개발팀",
		position="시니어",
		phone_number="010-1234-5678",
		episode_id=1
	)

	# When
	result = await user_command_service.register(request)

	# Then
	assert result.id is not None
	assert result.user_code == "TEST001"
	assert result.name == "홍길동"


@pytest.mark.asyncio
async def test_register_user_duplicate_user_code(user_command_service, user_repository):
	# Given
	existing_user = UserFixture.create_user(user_code="DUPLICATE001", name="기존유저")
	await user_repository.save(existing_user)

	request = UserRegisterRequest(
		user_code="DUPLICATE001",
		name="홍길동",
		department="개발팀",
		position="시니어",
		phone_number="010-1234-5678",
		episode_id=1
	)

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await user_command_service.register(request)

	assert exc_info.value.error_code == ErrorCode.USER_CODE_ALREADY_EXISTS
	assert "DUPLICATE001" in exc_info.value.message


@pytest.mark.asyncio
async def test_delete_user(user_command_service, user_repository):
	# Given
	user = UserFixture.create_user(user_code="TEST001", name="홍길동")
	saved_user = await user_repository.save(user)

	# When
	await user_command_service.delete(saved_user.id)

	# Then
	found_user = await user_repository.find_by_id(saved_user.id)
	assert found_user is None


@pytest.mark.asyncio
async def test_delete_user_not_found(user_command_service):
	# Given
	NON_EXISTENT_USER_ID = 9999

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await user_command_service.delete(NON_EXISTENT_USER_ID)

	assert exc_info.value.error_code == ErrorCode.USER_NOT_FOUND
