from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import User as TelegramUser
from telegram.ext import ContextTypes

from core.constants import LOGO_PNG_PATH
from text.messages import MAIN_PAGE_TEXT
from utils import get_or_create_current_user

# from utils.update_page import decorator_delete_pre_msg


# @decorator_delete_pre_msg
async def show_main_page(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Начальная страница."""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Подобрать оборудование", callback_data="select_equipment"
                )
            ],
            [
                InlineKeyboardButton(
                    "Связаться с Консультантом", callback_data="/communicate"
                )
            ],
        ]
    )
    tg_user: TelegramUser = update.effective_user

    await get_or_create_current_user(tg_user)

    with open(LOGO_PNG_PATH, "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=MAIN_PAGE_TEXT,
            parse_mode="HTML",
            reply_markup=buttons,
        )
