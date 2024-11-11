import os
from typing import Final

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.core.config import BASE_DIR
from src.core.db import Base
from src.models.administration_user import AdministrationUser
from src.models.user import User

TEST_DB_URL: Final[str] = BASE_DIR / "TEST_DB_URL.db"
SQLALCHEMY_DATABASE_URL: Final[str] = f"sqlite+aiosqlite:///{str(TEST_DB_URL)}"
engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession)


@pytest.fixture(scope="function")
def engine():
    """Need docstring."""
    engine: AsyncEngine = create_async_engine(
        os.environ[TEST_DB_URL], echo=False
    )
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine, checkfirst=True)


@pytest.fixture
async def session():
    """Test Async stssion."""
    async with TestingSessionLocal() as async_session:
        yield async_session


@pytest.fixture(scope="function")
async def test_create_user(session):
    """Создание тестового пользователя User."""
    user = User(
        tg_username="test_username",
        tg_chat_id=123456789,
        name="Test User",
        phone_number="+79160101010",
        email="test_user@test.ru",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def test_create_administration_user(session):
    """Создание тестового пользователя AdministrationUser."""
    admin_user = AdministrationUser(
        email="testuser@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_superuser=True,
        is_verified=True,
    )
    session.add(admin_user)
    await session.commit()
    await session.refresh(admin_user)
    return admin_user
