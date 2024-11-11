from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.password import PasswordHelper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import get_async_session
from models.administration_user import AdministrationUser
from schemas.administration_user import AdministrationUserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Асинхронный генератор доступа к БД."""
    yield SQLAlchemyUserDatabase(session, AdministrationUser)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """Need docstring."""
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[AdministrationUser, int]):
    """Need docstring."""

    async def validate_password(
        self,
        password: str,
        user: Union[AdministrationUserCreate, AdministrationUser],
    ) -> None:
        """Need docstring."""
        if len(password) < 3:
            raise InvalidPasswordException(
                reason="Пароль должен содержать, как минимум, 3 символа."
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Пароль не может содержать e-mail."
            )

    async def on_after_register(
        self, user: AdministrationUser, request: Optional[Request] = None
    ):
        """Вывод сообщения о регистрации."""
        print(f"Пользователь {user.email} зарегистрирован.")


password_hash = PasswordHash((Argon2Hasher(),))
password_helper = PasswordHelper(password_hash)


async def get_user_manager(user_db=Depends(get_user_db)):
    """Need docstring."""
    yield UserManager(user_db, password_helper)


fastapi_users = FastAPIUsers[AdministrationUser, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
