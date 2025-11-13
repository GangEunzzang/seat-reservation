from app.user.domain.user import User
from app.user.application.ports.inbound.commands import RegisterUserCommand


async def test_create_user():
	# Given
	request = RegisterUserCommand(
		user_code="U001",
		name="홍길동",
		department="개발팀",
		position="개발자",
		phone_number="010-1234-5678",
		episode_id=1
	)

	# When
	user = User.create(request)

	# Then
	assert user.user_code == "U001"
	assert user.name == "홍길동"
	assert user.id == 1
