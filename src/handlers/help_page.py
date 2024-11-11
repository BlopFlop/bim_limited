from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from core.constants import LOGO_PNG_PATH
from text.messages import HELP_PAGE_TEXT


async def show_help_page(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Страница справки."""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Вернуться на главную страницу", callback_data="/back"
                )
            ],
        ]
    )

    with open(LOGO_PNG_PATH, "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=HELP_PAGE_TEXT,
            parse_mode="HTML",
            reply_markup=buttons,
        )
