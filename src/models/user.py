from sqlalchemy import BigInteger, Column, String

from core.db import Base


class User(Base):
    """Модель пользователя (Telegram)."""

    tg_username = Column(
        String,
        nullable=False,
        unique=True,
        comment="Username пользователя в Telegram",
    )
    tg_chat_id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        comment="Идентификатор чата с пользователем в Telegram",
    )
    name = Column(String, nullable=True, comment="Имя пользователя")
    phone_number = Column(
        String, nullable=True, comment="Контактный номер телефона пользователя"
    )
    email = Column(
        String, nullable=True, comment="Контактный email-адрес пользователя"
    )

    def __repr__(self) -> str:
        return (
            f"<User({self.id}, "
            f"tg_username='{self.tg_username}', "
            f"email='{self.email}')>"
        )
