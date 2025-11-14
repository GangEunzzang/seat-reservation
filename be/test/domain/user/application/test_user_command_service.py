import pytest
from unittest.mock import AsyncMock, Mock

from app.domain.user.application.dto.user_command import RegisterUserCommand
from app.domain.user.application.user_command_service import UserCommandService
from app.domain.user.domain.user import User
from test.domain.user.user_fixture import UserFixture


@pytest.fixture
def mock_user_repository():
	"""Mock UserRepository"""
	return AsyncMock()


@pytest.fixture
def user_command_service(mock_user_repository):
	"""UserCommandService Fixture"""
	return UserCommandService(mock_user_repository)


@pytest.mark.asyncio
async def test_register_user(user_command_service, mock_user_repository):
	"""사용자 등록 테스트"""
	# Given
	command = RegisterUserCommand(
		user_code="TEST001",
		name="홍길동",
		department="개발팀",
		position="시니어",
		phone_number="010-1234-5678",
		episode_id=1
	)
	mock_user_repository.exists_by_user_code.return_value = False
	created_user = UserFixture.create_user(
		user_code=command.user_code,
		name=command.name,
		department=command.department,
		position=command.position,
		phone_number=command.phone_number,
		episode_id=command.episode_id
	)
	created_user.id = 1
	mock_user_repository.save.return_value = created_user

	# When
	result = await user_command_service.register(command)

	# Then
	assert result.id == 1
	assert result.user_code == "TEST001"
	assert result.name == "홍길동"
	mock_user_repository.exists_by_user_code.assert_called_once_with("TEST001")
	mock_user_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_register_user_duplicate_user_code(user_command_service, mock_user_repository):
	"""중복된 사용자 코드로 등록 시 실패 테스트"""
	# Given
	command = RegisterUserCommand(
		user_code="DUPLICATE001",
		name="홍길동",
		department="개발팀",
		position="시니어",
		phone_number="010-1234-5678",
		episode_id=1
	)
	mock_user_repository.exists_by_user_code.return_value = True

	# When & Then
	with pytest.raises(ValueError) as exc_info:
		await user_command_service.register(command)

	assert "already exists" in str(exc_info.value)
	mock_user_repository.exists_by_user_code.assert_called_once_with("DUPLICATE001")
	mock_user_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_delete_user(user_command_service, mock_user_repository):
	"""사용자 삭제 테스트"""
	# Given
	user_id = 1
	existing_user = UserFixture.create_user(user_code="TEST001", name="홍길동")
	existing_user.id = user_id
	mock_user_repository.find_by_id.return_value = existing_user
	mock_user_repository.delete.return_value = None

	# When
	await user_command_service.delete(user_id)

	# Then
	mock_user_repository.find_by_id.assert_called_once_with(user_id)
	mock_user_repository.delete.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_delete_user_not_found(user_command_service, mock_user_repository):
	"""존재하지 않는 사용자 삭제 시 실패 테스트"""
	# Given
	user_id = 9999
	mock_user_repository.find_by_id.return_value = None

	# When & Then
	with pytest.raises(ValueError) as exc_info:
		await user_command_service.delete(user_id)

	assert "not found" in str(exc_info.value)
	mock_user_repository.find_by_id.assert_called_once_with(user_id)
	mock_user_repository.delete.assert_not_called()
