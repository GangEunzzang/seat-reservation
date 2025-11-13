import pytest
import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app

TEST_DB_URL = "sqlite:///:memory:"
os.environ["ENVIRONMENT"] = "test"

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    return engine

@pytest.fixture(scope="function")
def db_session(db_engine):
    """각 테스트마다 새로운 DB 세션 제공"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()