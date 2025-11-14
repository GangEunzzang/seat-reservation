import pytest
from unittest.mock import AsyncMock

from app.core.exceptions import DomainException, ErrorCode
from app.domain.user.application.user_command_service import UserCommandService
from app.domain.user.domain.user_register_request import UserRegisterRequest
from test.domain.user.user_fixture import UserFixture


@pytest.fixture
def mock_user_repository():
	return AsyncMock()


@pytest.fixture
def user_command_service(mock_user_repository):
	return UserCommandService(mock_user_repository)


@pytest.mark.asyncio
async def test_register_user(user_command_service, mock_user_repository):
	# Given
	request = UserRegisterRequest(
		user_code="TEST001",
		name="홍길동",
		department="개발팀",
		position="시니어",
		phone_number="010-1234-5678",
		episode_id=1
	)
	mock_user_repository.exists_by_user_code.return_value = False
	created_user = UserFixture.create_user(
		user_code=request.user_code,
		name=request.name,
		department=request.department,
		position=request.position,
		phone_number=request.phone_number,
		episode_id=request.episode_id
	)
	created_user.id = 1
	mock_user_repository.save.return_value = created_user

	# When
	result = await user_command_service.register(request)

	# Then
	assert result.id == 1
	assert result.user_code == "TEST001"
	assert result.name == "홍길동"
	mock_user_repository.exists_by_user_code.assert_called_once_with("TEST001")
	mock_user_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_register_user_duplicate_user_code(user_command_service, mock_user_repository):
	# Given
	request = UserRegisterRequest(
		user_code="DUPLICATE001",
		name="홍길동",
		department="개발팀",
		position="시니어",
		phone_number="010-1234-5678",
		episode_id=1
	)
	mock_user_repository.exists_by_user_code.return_value = True

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await user_command_service.register(request)

	assert exc_info.value.error_code == ErrorCode.USER_CODE_ALREADY_EXISTS
	assert "DUPLICATE001" in exc_info.value.message
	mock_user_repository.exists_by_user_code.assert_called_once_with("DUPLICATE001")
	mock_user_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_delete_user(user_command_service, mock_user_repository):
	# Given
	user_id = 1
	existing_user = UserFixture.create_user(user_code="TEST001", name="홍길동")
	existing_user.id = user_id
	mock_user_repository.find_by_id.return_value = existing_user

	# When
	await user_command_service.delete(user_id)

	# Then
	mock_user_repository.find_by_id.assert_called_once_with(user_id)
	mock_user_repository.delete.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_delete_user_not_found(user_command_service, mock_user_repository):
	# Given
	user_id = 9999
	mock_user_repository.find_by_id.return_value = None

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await user_command_service.delete(user_id)

	assert exc_info.value.error_code == ErrorCode.USER_NOT_FOUND
	mock_user_repository.find_by_id.assert_called_once_with(user_id)
	mock_user_repository.delete.assert_not_called()
