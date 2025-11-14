import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.adapter.outbound.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from test.domain.user.user_fixture import UserFixture


@pytest.fixture
def user_repository(async_session: AsyncSession) -> SQLAlchemyUserRepository:
	"""UserRepository 구현체 Fixture (conftest.py의 async_session 주입받음)"""
	return SQLAlchemyUserRepository(async_session)


@pytest.mark.asyncio
async def test_save_user(user_repository):
	"""User 저장 테스트"""
	# Given
	user = UserFixture.create_user(user_code="TEST001", name="홍길동")

	# When
	saved_user = await user_repository.save(user)

	# Then
	assert saved_user.id is not None
	assert saved_user.user_code == "TEST001"
	assert saved_user.name == "홍길동"


@pytest.mark.asyncio
async def test_find_by_id(user_repository):
	"""ID로 User 조회 테스트"""
	# Given
	user = UserFixture.create_user(user_code="TEST002", name="김철수")
	saved_user = await user_repository.save(user)

	# When
	found_user = await user_repository.find_by_id(saved_user.id)

	# Then
	assert found_user is not None
	assert found_user.id == saved_user.id
	assert found_user.user_code == "TEST002"
	assert found_user.name == "김철수"


@pytest.mark.asyncio
async def test_find_by_id_not_found(user_repository):
	"""존재하지 않는 ID로 조회 시 None 반환 테스트"""
	# Given
	NON_EXISTENT_USER_ID = 9999

	# When
	found_user = await user_repository.find_by_id(NON_EXISTENT_USER_ID)

	# Then
	assert found_user is None


@pytest.mark.asyncio
async def test_find_by_user_code(user_repository):
	"""user_code로 User 조회 테스트"""
	# Given
	user = UserFixture.create_user(user_code="UNIQUE001", name="이영희")
	await user_repository.save(user)

	# When
	found_user = await user_repository.find_by_user_code("UNIQUE001")

	# Then
	assert found_user is not None
	assert found_user.user_code == "UNIQUE001"
	assert found_user.name == "이영희"


@pytest.mark.asyncio
async def test_find_by_user_code_not_found(user_repository):
	"""존재하지 않는 user_code로 조회 시 None 반환 테스트"""
	# When
	found_user = await user_repository.find_by_user_code("NOTEXIST")

	# Then
	assert found_user is None


@pytest.mark.asyncio
async def test_find_all(user_repository):
	"""모든 User 조회 테스트"""
	# Given
	user1 = UserFixture.create_user(user_code="USER001", name="사용자1")
	user2 = UserFixture.create_user(user_code="USER002", name="사용자2")
	user3 = UserFixture.create_user(user_code="USER003", name="사용자3")

	await user_repository.save(user1)
	await user_repository.save(user2)
	await user_repository.save(user3)

	# When
	users = await user_repository.find_all()

	# Then
	assert len(users) == 3
	user_codes = [u.user_code for u in users]
	assert "USER001" in user_codes
	assert "USER002" in user_codes
	assert "USER003" in user_codes


@pytest.mark.asyncio
async def test_delete(user_repository):
	"""User 삭제 테스트"""
	# Given
	user = UserFixture.create_user(user_code="DELETE001", name="삭제대상")
	saved_user = await user_repository.save(user)

	# When
	await user_repository.delete(saved_user.id)

	# Then
	found_user = await user_repository.find_by_id(saved_user.id)
	assert found_user is None


@pytest.mark.asyncio
async def test_exists_by_user_code_true(user_repository):
	"""user_code 존재 여부 확인 테스트 (존재하는 경우)"""
	# Given
	user = UserFixture.create_user(user_code="EXISTS001", name="존재함")
	await user_repository.save(user)

	# When
	exists = await user_repository.exists_by_user_code("EXISTS001")

	# Then
	assert exists is True


@pytest.mark.asyncio
async def test_exists_by_user_code_false(user_repository):
	"""user_code 존재 여부 확인 테스트 (존재하지 않는 경우)"""
	# When
	exists = await user_repository.exists_by_user_code("NOTEXIST")

	# Then
	assert exists is False
