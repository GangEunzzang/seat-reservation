import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.adapter.outbound.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.user.application.user_query_service import UserQueryService
from core.exception.domain_exception import DomainException
from core.exception.error_code import ErrorCode
from test.app.user.user_fixture import UserFixture


@pytest.fixture
def user_repository(async_session: AsyncSession) -> SQLAlchemyUserRepository:
	return SQLAlchemyUserRepository(async_session)


@pytest.fixture
def user_query_service(user_repository) -> UserQueryService:
	return UserQueryService(user_repository)


@pytest.mark.asyncio
async def test_get_user_by_id(user_query_service, user_repository):
	# Given
	user = UserFixture.create_user(name="홍길동")
	saved_user = await user_repository.save(user)

	# When
	result = await user_query_service.get_user_by_id(saved_user.id)

	# Then
	assert result is not None
	assert result.id == saved_user.id
	assert result.name == "홍길동"


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_query_service):
	# Given
	NON_EXISTENT_USER_ID = 9999

	# When & Then
	with pytest.raises(DomainException) as exc_info:
		await user_query_service.get_user_by_id(NON_EXISTENT_USER_ID)

	assert exc_info.value.error_code == ErrorCode.USER_NOT_FOUND


@pytest.mark.asyncio
async def test_get_user_list_all(user_query_service, user_repository):
	# Given
	users = [
		UserFixture.create_user(name="사용자1"),
		UserFixture.create_user(name="사용자2"),
		UserFixture.create_user(name="사용자3"),
	]
	for user in users:
		await user_repository.save(user)

	# When
	result = await user_query_service.get_user_list_all()

	# Then
	assert len(result) == 3
	user_names = [u.name for u in result]
	assert "사용자1" in user_names
	assert "사용자2" in user_names
	assert "사용자3" in user_names


@pytest.mark.asyncio
async def test_get_user_list_all_empty(user_query_service):
	# When
	result = await user_query_service.get_user_list_all()

	# Then
	assert result == []
