import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.deps import get_db


# =========================
# Test Database Configuration
# =========================

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture(scope="session")
def api_prefix() -> str:
    """
    API 공통 prefix
    """
    return "/api/v1"


# =========================
# Dependency Override
# =========================

def override_get_db():
    """
    테스트용 DB dependency

    - 테스트 함수 단위로 트랜잭션을 열고
    - API 내부에서 commit이 발생해도
    - 테스트 종료 시 전체 rollback
    """
    connection = engine.connect()
    transaction = connection.begin()

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()


# =========================
# Database Schema Fixture
# =========================

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    테스트 전체에서 한 번만:
    - 테이블 생성
    - 테스트 종료 후 테이블 제거
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# =========================
# TestClient Fixture
# =========================

@pytest.fixture(scope="function")
def client():
    """
    각 테스트 함수마다:
    - get_db dependency override 적용
    - TestClient 제공
    - 테스트 종료 후 override 제거
    """
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
