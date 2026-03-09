"""Pytest fixtures."""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import async_engine, Base, AsyncSessionLocal
from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_database() -> AsyncGenerator[None, None]:
    """Create test database."""
    # Create in-memory SQLite for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(test_database) -> AsyncGenerator[AsyncSession, None]:
    """Create database session for tests."""
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
def client(db_session) -> TestClient:
    """Create test client."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[DatabaseDependency] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
