from typing import Optional

from pydantic import BaseModel, Field


class UserSchemaBase(BaseModel):
    """Base user schema."""

    tg_username: str = Field(
        title="tg_username", description="Username пользователя в Telegram"
    )
    tg_chat_id: int = Field(
        title="tg_chat_id",
        description="Идентификатор чата с пользователем в Telegram",
    )
    name: Optional[str] = Field(
        None, title="name", description="Имя пользователя"
    )
    phone_number: Optional[str] = Field(
        None,
        title="phone_number",
        description="Контактный номер телефона пользователя",
    )
    email: Optional[str] = Field(
        None, title="email", description="Контактный email-адрес пользователя"
    )


class UserSchemaCreate(UserSchemaBase):
    """Create user schema."""

    pass


class UserSchemaUpdate(UserSchemaBase):
    """Update user schema."""

    tg_username: Optional[str] = Field(
        None,
        title="tg_username",
        description="Username пользователя в Telegram",
    )
    tg_chat_id: Optional[str] = Field(
        None,
        title="tg_chat_id",
        description="Идентификатор чата с пользователем в Telegram",
    )


class UserSchemaDB(UserSchemaBase):
    """Result user schema."""

    id: int = Field(
        title="Id TG User in db",
        description="Id Телеграм юзера в базе данных.",
    )

    class Config:
        """Config for this schemas."""

        orm_mode: bool = True
