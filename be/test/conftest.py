import os

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config.database import Base, get_async_session
from app.main import app

TEST_DB_URL = "sqlite:///:memory:"
TEST_ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"
os.environ["ENVIRONMENT"] = "test"


@pytest.fixture
def client():
	"""FastAPI TestClient"""
	return TestClient(app)


@pytest.fixture(scope="session")
def db_engine():
	"""테스트용 DB 엔진 (세션 스코프)"""
	engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
	return engine


@pytest.fixture(scope="function")
def db_session(db_engine) -> Session:
	"""각 테스트마다 새로운 동기 DB 세션 제공"""
	TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
	session = TestingSessionLocal()
	yield session
	session.rollback()
	session.close()


@pytest.fixture(scope="function")
async def async_session() -> AsyncSession:
	"""각 테스트마다 새로운 비동기 DB 세션 제공"""
	# 테스트용 비동기 엔진 생성
	async_engine = create_async_engine(
		TEST_ASYNC_DB_URL,
		echo=False
	)

	# DB 초기화 (테이블 생성)
	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

	# 세션 생성
	AsyncTestingSessionLocal = async_sessionmaker(
		bind=async_engine,
		class_=AsyncSession,
		expire_on_commit=False,
		autoflush=False,
		autocommit=False,
	)

	async with AsyncTestingSessionLocal() as session:
		yield session
		await session.rollback()

	# DB 정리 (테이블 삭제)
	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)

	await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_client():
	"""비동기 HTTP 클라이언트 with 테스트 DB"""
	async_engine = create_async_engine(TEST_ASYNC_DB_URL, echo=False)

	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

	AsyncTestingSessionLocal = async_sessionmaker(
		bind=async_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
	)

	async def override_get_async_session():
		async with AsyncTestingSessionLocal() as session:
			try:
				yield session
				await session.commit()
			except Exception:
				await session.rollback()
				raise

	app.dependency_overrides[get_async_session] = override_get_async_session

	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url="http://test") as ac:
		yield ac

	app.dependency_overrides.clear()

	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)

	await async_engine.dispose()
