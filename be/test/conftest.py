"""
공통 테스트 Fixture

DB 세션, API 클라이언트 등 공통으로 사용되는 fixture만 정의합니다.
각 도메인별 fixture는 각 도메인의 conftest.py에 정의합니다.
"""

import pytest
import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app

TEST_DB_URL = "sqlite:///:memory:"
os.environ["ENVIRONMENT"] = "test"


# ============================================================================
# API Client Fixtures
# ============================================================================

@pytest.fixture
def client():
	"""FastAPI TestClient"""
	return TestClient(app)


# ============================================================================
# Database Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def db_engine():
	"""테스트용 DB 엔진 (세션 스코프)"""
	engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
	return engine


@pytest.fixture(scope="function")
def db_session(db_engine) -> Session:
	"""각 테스트마다 새로운 DB 세션 제공"""
	TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
	session = TestingSessionLocal()
	yield session
	session.rollback()
	session.close()
