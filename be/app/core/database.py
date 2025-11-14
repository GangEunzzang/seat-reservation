"""
비동기 SQLAlchemy 데이터베이스 설정

헥사고날 아키텍처에서 Infrastructure 계층에 해당하는 공통 데이터베이스 설정입니다.
"""

from typing import AsyncGenerator

import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# 환경별 DATABASE_URL 설정 (향후 환경변수로 관리)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# 환경변수에 따라 SQL 로그 출력 여부 결정
SQL_ECHO = os.getenv("SQL_ECHO", "True").lower() in ("true", "1", "yes")

# AsyncEngine 생성
async_engine = create_async_engine(
	DATABASE_URL,
	echo=SQL_ECHO,  # SQL 로그 출력 (환경에 따라 결정)
	future=True,
)

# AsyncSessionLocal: 비동기 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
	bind=async_engine,
	class_=AsyncSession,
	expire_on_commit=False,
	autoflush=False,
	autocommit=False,
)


class Base(DeclarativeBase):
	"""모든 도메인 엔티티의 Base 클래스"""
	pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
	"""
	비동기 데이터베이스 세션을 제공하는 Dependency

	FastAPI에서 Depends()로 사용됩니다.
	헥사고날 아키텍처에서 Outbound Adapter가 이 세션을 사용합니다.
	"""
	async with AsyncSessionLocal() as session:
		try:
			yield session
			await session.commit()
		except Exception:
			await session.rollback()
			raise
		finally:
			await session.close()


async def init_db() -> None:
	"""
	데이터베이스 테이블 생성

	개발/테스트 환경에서만 사용. 운영 환경에서는 Alembic 사용 권장.
	"""
	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
	"""
	데이터베이스 테이블 삭제

	테스트 환경에서만 사용.
	"""
	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
