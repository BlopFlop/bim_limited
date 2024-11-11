from typing import Any, Callable

from telegram import Update
from telegram import User as TelegramUser
from telegram.ext import ConversationHandler

from core.db import AsyncSessionLocal
from models import User
from repository import user_repository
from schemas import UserSchemaCreate


async def get_or_create_current_user(tg_user: TelegramUser) -> User:
    """Get user, before checking user in db."""
    user_schema_create = UserSchemaCreate(
        tg_username=tg_user.username, tg_chat_id=tg_user.id
    )
    async with AsyncSessionLocal() as session:
        user_repository.session = session

        user_obj = await user_repository.get_obj_for_field_arg(
            field="tg_chat_id", arg=tg_user.id, many=False
        )
    if not user_obj:
        return await user_repository.create(user_schema_create)
    return user_obj


def remove_current_user_convesate(
    user: TelegramUser, conversations: dict[tuple[int, int], str]
) -> None:
    """Remove user.id in handler._convestae."""
    if conversations:
        conversations_current_user = [
            conversate
            for conversate in conversations.keys()
            if user.id in conversate
        ]
        if conversations_current_user:
            for conversate in conversations_current_user:
                conversations.pop(conversate)


def remove_user_convesate(get_contacts_handler: ConversationHandler):
    """Remove conversate user."""

    def decorator(func: Callable):
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            update: Update = args[0]

            remove_current_user_convesate(
                update.effective_user, get_contacts_handler._conversations
            )
            return await func(*args, **kwargs)

        return wrapper

    return decorator
