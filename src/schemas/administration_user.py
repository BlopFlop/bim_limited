from fastapi_users import schemas


class AdministrationUserRead(schemas.BaseUser[int]):
    """Базовая схема для чтения пользователя."""

    pass


class AdministrationUserCreate(schemas.BaseUserCreate):
    """Базовая схема для создания пользователя."""

    pass


class AdministrationUserUpdate(schemas.BaseUserUpdate):
    """Базовая схема для обновления пользователя."""

    pass
