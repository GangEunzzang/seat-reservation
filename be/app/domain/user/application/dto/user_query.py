from dataclasses import dataclass


@dataclass
class GetUserByIdQuery:
	"""ID로 사용자 조회 쿼리"""
	user_id: int


@dataclass
class GetUserByCodeQuery:
	"""사용자 코드로 조회 쿼리"""
	user_code: str
