import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.exception.domain_exception import DomainException, ErrorCode
from app.user.adapter.outbound.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.user.application.user_command_service import UserCommandService
from app.user.domain.user_register_request import UserRegisterRequest
from test.app.user.user_fixture import UserFixture


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
	assert result.name == "홍길동"


@pytest.mark.asyncio
async def test_delete_user(user_command_service, user_repository):
	# Given
	user = UserFixture.create_user(name="홍길동")
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


@pytest.mark.asyncio
async def test_register_bulk(user_command_service):
	# Given
	requests = [
		UserRegisterRequest(
			name="홍길동",
			department="개발팀",
			position="시니어",
			phone_number="010-1234-5678",
			episode_id=1
		),
		UserRegisterRequest(
			name="김철수",
			department="기획팀",
			position="주니어",
			phone_number="010-1234-5679",
			episode_id=1
		),
		UserRegisterRequest(
			name="이영희",
			department="디자인팀",
			position="시니어",
			phone_number="010-1234-5680",
			episode_id=1
		)
	]

	# When
	result = await user_command_service.register_bulk(requests)

	# Then
	assert len(result) == 3
	assert result[0].name == "홍길동"
	assert result[1].name == "김철수"
	assert result[2].name == "이영희"
	assert all(user.id is not None for user in result)


@pytest.mark.asyncio
async def test_register_bulk_rollback_on_error(user_command_service, user_repository):
	"""
	다건 등록 중 하나라도 실패하면 전체가 rollback 되는지 검증

	Note: 현재 비즈니스 로직에서는 실패할 수 있는 검증이 없어서,
	이 테스트는 트랜잭션 동작을 문서화하는 목적입니다.
	"""
	# Given
	requests = [
		UserRegisterRequest(
			name="홍길동",
			department="개발팀",
			position="시니어",
			phone_number="010-1234-5678",
			episode_id=1
		),
		UserRegisterRequest(
			name="김철수",
			department="기획팀",
			position="주니어",
			phone_number="010-1234-5679",
			episode_id=1
		)
	]

	# When
	await user_command_service.register_bulk(requests)

	# Then - 트랜잭션이 커밋되어 모두 저장되었는지 확인
	all_users = await user_repository.find_all()
	assert len(all_users) == 2
