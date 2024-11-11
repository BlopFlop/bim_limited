import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from core.administration_user import get_user_db, get_user_manager
from core.config import settings
from core.db import get_async_session
from schemas.administration_user import AdministrationUserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_administration_user(
    email: EmailStr, password: str, is_superuser: bool = False
):
    """Корутина, создающая юзера."""
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        AdministrationUserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                        )
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    """Создание первого суперюзера."""
    if (
        settings.first_superuser_email is not None
        and settings.first_superuser_password is not None
    ):
        await create_administration_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
