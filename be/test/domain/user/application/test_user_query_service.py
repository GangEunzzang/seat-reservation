import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.adapter.outbound.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.user.application.user_query_service import UserQueryService
from test.domain.user.user_fixture import UserFixture


@pytest.fixture
def user_repository(async_session: AsyncSession) -> SQLAlchemyUserRepository:
	return SQLAlchemyUserRepository(async_session)


@pytest.fixture
def user_query_service(user_repository) -> UserQueryService:
	return UserQueryService(user_repository)


@pytest.mark.asyncio
async def test_get_user_by_id(user_query_service, user_repository):
	# Given
	user = UserFixture.create_user(user_code="TEST001", name="홍길동")
	saved_user = await user_repository.save(user)

	# When
	result = await user_query_service.get_user_by_id(saved_user.id)

	# Then
	assert result is not None
	assert result.id == saved_user.id
	assert result.user_code == "TEST001"
	assert result.name == "홍길동"


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_query_service):
	# Given
	NON_EXISTENT_USER_ID = 9999

	# When
	result = await user_query_service.get_user_by_id(NON_EXISTENT_USER_ID)

	# Then
	assert result is None


@pytest.mark.asyncio
async def test_get_user_by_code(user_query_service, user_repository):
	# Given
	user = UserFixture.create_user(user_code="TEST001", name="홍길동")
	await user_repository.save(user)

	# When
	result = await user_query_service.get_user_by_code("TEST001")

	# Then
	assert result is not None
	assert result.user_code == "TEST001"
	assert result.name == "홍길동"


@pytest.mark.asyncio
async def test_get_user_by_code_not_found(user_query_service):
	# Given
	NON_EXISTENT_USER_CODE = "NOTEXIST"

	# When
	result = await user_query_service.get_user_by_code(NON_EXISTENT_USER_CODE)

	# Then
	assert result is None


@pytest.mark.asyncio
async def test_get_user_list_all(user_query_service, user_repository):
	# Given
	users = [
		UserFixture.create_user(user_code="USER001", name="사용자1"),
		UserFixture.create_user(user_code="USER002", name="사용자2"),
		UserFixture.create_user(user_code="USER003", name="사용자3"),
	]
	for user in users:
		await user_repository.save(user)

	# When
	result = await user_query_service.get_user_list_all()

	# Then
	assert len(result) == 3
	assert result[0].user_code == "USER001"
	assert result[1].user_code == "USER002"
	assert result[2].user_code == "USER003"


@pytest.mark.asyncio
async def test_get_user_list_all_empty(user_query_service):
	# When
	result = await user_query_service.get_user_list_all()

	# Then
	assert result == []


@pytest.mark.asyncio
async def test_exists_by_user_code_true(user_query_service, user_repository):
	# Given
	user = UserFixture.create_user(user_code="EXISTS001", name="존재하는유저")
	await user_repository.save(user)

	# When
	result = await user_query_service.exists_by_user_code("EXISTS001")

	# Then
	assert result is True


@pytest.mark.asyncio
async def test_exists_by_user_code_false(user_query_service):
	# Given
	NON_EXISTENT_USER_CODE = "NOTEXIST"

	# When
	result = await user_query_service.exists_by_user_code(NON_EXISTENT_USER_CODE)

	# Then
	assert result is False
