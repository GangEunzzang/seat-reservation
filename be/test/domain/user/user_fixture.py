"""User 도메인 테스트 Fixture"""

from app.user.domain.user import User
from app.user.domain.user_register_request import UserRegisterRequest


class UserFixture:
	"""User 도메인 테스트 데이터 생성 헬퍼"""

	@staticmethod
	def create_user_register_request(
		user_code: str = "TEST001",
		name: str = "테스트유저",
		department: str = "테스트부서",
		position: str = "테스트직책",
		phone_number: str = "010-1234-5678",
		episode_id: int = 1
	) -> UserRegisterRequest:
		"""UserRegisterRequest 생성"""
		return UserRegisterRequest(
			user_code=user_code,
			name=name,
			department=department,
			position=position,
			phone_number=phone_number,
			episode_id=episode_id
		)

	@staticmethod
	def create_user(
		user_code: str = "TEST001",
		name: str = "테스트유저",
		department: str = "테스트부서",
		position: str = "테스트직책",
		phone_number: str = "010-1234-5678",
		episode_id: int = 1
	) -> User:
		"""User 엔티티 생성"""
		request = UserFixture.create_user_register_request(
			user_code=user_code,
			name=name,
			department=department,
			position=position,
			phone_number=phone_number,
			episode_id=episode_id
		)
		return User.create(request)

	@staticmethod
	def create_multiple_users(count: int = 3) -> list[User]:
		"""여러 명의 User 엔티티 생성"""
		users = []
		for i in range(1, count + 1):
			user = UserFixture.create_user(
				user_code=f"USER{i:03d}",
				name=f"사용자{i}",
				department=f"부서{i}",
				position="직원",
				phone_number=f"010-0000-{i:04d}",
				episode_id=1
			)
			users.append(user)
		return users
