from typing import Any, Callable

from telegram import Update
from telegram.ext import ContextTypes


def decorator_delete_pre_msg(func: Callable):
    """Декоратор удаляющий предыдущие сообщения."""

    async def wrapper(*args: Any, **kwargs: Any):
        update: Update = args[0]
        context: ContextTypes.DEFAULT_TYPE = args[1]

        result = await func(*args, **kwargs)

        if update.callback_query and update.callback_query.data == "no_action":
            return result

        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=update.effective_message.message_id,
            )
        except Exception:
            pass

        return result

    return wrapper


def message_control_dialog(
    context: ContextTypes.DEFAULT_TYPE, message=None
) -> list[int]:
    """Добавляет все сообщения в кэш, чтобы его потом удалить."""
    key_message = 'last_bot_message'

    if message:
        if key_message in context.bot_data:
            context.bot_data[key_message].append(message.message_id)
        else:
            context.bot_data[key_message] = [message.message_id]

    return context.bot_data[key_message]
