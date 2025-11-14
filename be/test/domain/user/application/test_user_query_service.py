import pytest
from unittest.mock import AsyncMock

from app.domain.user.application.user_query_service import UserQueryService
from test.domain.user.user_fixture import UserFixture


@pytest.fixture
def mock_user_repository():
	"""Mock UserRepository"""
	return AsyncMock()


@pytest.fixture
def user_query_service(mock_user_repository):
	"""UserQueryService Fixture"""
	return UserQueryService(mock_user_repository)


@pytest.mark.asyncio
async def test_get_user_by_id(user_query_service, mock_user_repository):
	"""ID로 사용자 조회 테스트"""
	# Given
	user_id = 1
	expected_user = UserFixture.create_user(user_code="TEST001", name="홍길동")
	expected_user.id = user_id
	mock_user_repository.find_by_id.return_value = expected_user

	# When
	result = await user_query_service.get_user_by_id(user_id)

	# Then
	assert result is not None
	assert result.id == user_id
	assert result.user_code == "TEST001"
	assert result.name == "홍길동"
	mock_user_repository.find_by_id.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_query_service, mock_user_repository):
	"""존재하지 않는 ID로 조회 시 None 반환 테스트"""
	# Given
	user_id = 9999
	mock_user_repository.find_by_id.return_value = None

	# When
	result = await user_query_service.get_user_by_id(user_id)

	# Then
	assert result is None
	mock_user_repository.find_by_id.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_user_by_code(user_query_service, mock_user_repository):
	"""사용자 코드로 조회 테스트"""
	# Given
	user_code = "TEST001"
	expected_user = UserFixture.create_user(user_code=user_code, name="홍길동")
	expected_user.id = 1
	mock_user_repository.find_by_user_code.return_value = expected_user

	# When
	result = await user_query_service.get_user_by_code(user_code)

	# Then
	assert result is not None
	assert result.user_code == user_code
	assert result.name == "홍길동"
	mock_user_repository.find_by_user_code.assert_called_once_with(user_code)


@pytest.mark.asyncio
async def test_get_user_by_code_not_found(user_query_service, mock_user_repository):
	"""존재하지 않는 사용자 코드로 조회 시 None 반환 테스트"""
	# Given
	user_code = "NOTEXIST"
	mock_user_repository.find_by_user_code.return_value = None

	# When
	result = await user_query_service.get_user_by_code(user_code)

	# Then
	assert result is None
	mock_user_repository.find_by_user_code.assert_called_once_with(user_code)


@pytest.mark.asyncio
async def test_list_users(user_query_service, mock_user_repository):
	"""전체 사용자 목록 조회 테스트"""
	# Given
	user1 = UserFixture.create_user(user_code="USER001", name="사용자1")
	user1.id = 1
	user2 = UserFixture.create_user(user_code="USER002", name="사용자2")
	user2.id = 2
	user3 = UserFixture.create_user(user_code="USER003", name="사용자3")
	user3.id = 3
	mock_user_repository.find_all.return_value = [user1, user2, user3]

	# When
	result = await user_query_service.get_user_list_all()

	# Then
	assert len(result) == 3
	assert result[0].user_code == "USER001"
	assert result[1].user_code == "USER002"
	assert result[2].user_code == "USER003"
	mock_user_repository.find_all.assert_called_once()


@pytest.mark.asyncio
async def test_list_users_empty(user_query_service, mock_user_repository):
	"""사용자가 없을 때 빈 목록 반환 테스트"""
	# Given
	mock_user_repository.find_all.return_value = []

	# When
	result = await user_query_service.get_user_list_all()

	# Then
	assert len(result) == 0
	mock_user_repository.find_all.assert_called_once()


@pytest.mark.asyncio
async def test_exists_by_user_code_true(user_query_service, mock_user_repository):
	"""사용자 코드 존재 여부 확인 테스트 (존재하는 경우)"""
	# Given
	user_code = "EXISTS001"
	mock_user_repository.exists_by_user_code.return_value = True

	# When
	result = await user_query_service.exists_by_user_code(user_code)

	# Then
	assert result is True
	mock_user_repository.exists_by_user_code.assert_called_once_with(user_code)


@pytest.mark.asyncio
async def test_exists_by_user_code_false(user_query_service, mock_user_repository):
	"""사용자 코드 존재 여부 확인 테스트 (존재하지 않는 경우)"""
	# Given
	user_code = "NOTEXIST"
	mock_user_repository.exists_by_user_code.return_value = False

	# When
	result = await user_query_service.exists_by_user_code(user_code)

	# Then
	assert result is False
	mock_user_repository.exists_by_user_code.assert_called_once_with(user_code)
