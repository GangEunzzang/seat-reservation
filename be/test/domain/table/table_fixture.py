"""Table 도메인 테스트 Fixture"""

from app.domain.table.domain.table import Table


class TableFixture:
	"""Table 도메인 테스트 데이터 생성 헬퍼"""

	@staticmethod
	def create_table(episode_id: int = 1) -> Table:
		"""Table 엔티티 생성"""
		return Table.create(episode_id=episode_id)

	@staticmethod
	def create_multiple_tables(episode_id: int = 1, count: int = 5) -> list[Table]:
		"""여러 개의 Table 엔티티 생성"""
		tables = []
		for _ in range(count):
			table = TableFixture.create_table(episode_id=episode_id)
			tables.append(table)
		return tables
