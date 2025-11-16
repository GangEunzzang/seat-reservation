"""Table 도메인 테스트 Fixture"""
from httpx import AsyncClient

from app.table.domain.table import Table


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

	@staticmethod
	def create_request_dict(episode_id: int = 1) -> dict:
		"""API 요청 body dict 생성"""
		return {"episode_id": episode_id}

	@staticmethod
	async def create_via_api(client: AsyncClient, episode_id: int = 1) -> dict:
		"""API를 통해 테이블 생성 후 응답 데이터 반환"""
		request_data = TableFixture.create_request_dict(episode_id)
		response = await client.post("/api/v1/table", json=request_data)
		return response.json()["data"]

	@staticmethod
	async def create_multiple_via_api(client: AsyncClient, episode_id: int = 1, count: int = 5) -> list[dict]:
		"""API를 통해 여러 테이블 생성"""
		tables = []
		for _ in range(count):
			table = await TableFixture.create_via_api(client, episode_id)
			tables.append(table)
		return tables
