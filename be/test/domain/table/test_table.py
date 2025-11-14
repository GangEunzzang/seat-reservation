from test.domain.table.table_fixture import TableFixture


def test_create_table():
	"""Table 생성 테스트"""
	# Given & When
	table = TableFixture.create_table(episode_id=1)

	# Then
	assert table.episode_id == 1
