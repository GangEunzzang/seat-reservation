from test.app.user.user_fixture import UserFixture


def test_create_user():
	"""User 생성 테스트"""
	# Given & When
	user = UserFixture.create_user(
		name="홍길동",
		department="개발팀",
		position="개발자",
		phone_number="010-1234-5678",
		episode_id=1
	)

	# Then
	assert user.name == "홍길동"
	assert user.department == "개발팀"
	assert user.position == "개발자"
	assert user.phone_number == "010-1234-5678"
	assert user.episode_id == 1
