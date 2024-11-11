from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from core.config import settings
from core.constants import (
    LOGO_PNG_PATH,
    RE_PATTERN_EMAIL,
    RE_PATTERN_NAME,
    RE_PATTERN_NUMBER_PHONE,
)
from core.db import AsyncSessionLocal
from repository import user_repository
from schemas import UserSchemaUpdate
from text.communicate import (
    ADD_EMAIL_TEXT,
    ADD_NAME_TEXT,
    ADD_NUMBER_TEXT,
    COMMUNICATE_TEXT,
    END_ADD_INFO_TEXT,
    EXCEPT_ADD_NAME_TEXT,
    EXCEPT_ADD_NUMBER_TEXT,
    EXCEPT_EMAIL_TEXT,
    READD_NUMBER_TEXT,
)
from utils import get_or_create_current_user, is_valid_pattern
from utils.update_page import decorator_delete_pre_msg, message_control_dialog

ADD_EMAIL_KEY = "add_email"
ADD_NUMBER_KEY = "add_number"
ADD_NAME_KEY = "add_name"


@decorator_delete_pre_msg
async def show_contacts_page(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Страница контактов."""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Сайт", url=settings.consultate_url),
                InlineKeyboardButton(
                    "Телеграм", url=settings.consultate_telegram
                ),
            ],
            [
                InlineKeyboardButton(
                    "Оставить контакты", callback_data="/add_contacts"
                )
            ],
            [
                InlineKeyboardButton(
                    "Вернуться на главную страницу", callback_data="/back"
                )
            ],
        ]
    )

    with open(LOGO_PNG_PATH, "rb") as photo:
        await update.effective_chat.send_photo(
            photo=photo,
            caption=COMMUNICATE_TEXT.format(
                settings.consultate_mail, settings.consultate_number
            ),
            parse_mode="HTML",
            reply_markup=buttons,
        )


@decorator_delete_pre_msg
async def start_add_contacts(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Старт ввода контактов пользователя."""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "На страницу назад >> Контакты / Консультация",
                    callback_data="/communicate",
                )
            ],
            [
                InlineKeyboardButton(
                    "Вернуться на главную страницу", callback_data="/back"
                )
            ],
        ]
    )

    current_user = await get_or_create_current_user(update.effective_user)

    email = current_user.email
    name = current_user.name
    phone_number = current_user.phone_number

    if all((email, name, phone_number)):
        message = await update.effective_message.reply_text(
            READD_NUMBER_TEXT.format(name, phone_number, email),
            reply_markup=buttons,
        )
    else:
        message = await update.effective_message.reply_text(
            ADD_NUMBER_TEXT, reply_markup=buttons
        )

    message_control_dialog(context, message)

    return ADD_NUMBER_KEY


async def show_add_name_page(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Ввод имени пользователя."""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "На страницу назад >> Ввод номера",
                    callback_data="/back_page",
                )
            ],
            [
                InlineKeyboardButton(
                    "Вернуться на главную страницу", callback_data="/back"
                )
            ],
        ]
    )

    if update.message is None:
        phone_number = context.user_data["phone_number"]
    else:
        message_control_dialog(context, update.message)
        phone_number = update.message.text

    if is_valid_pattern(phone_number, RE_PATTERN_NUMBER_PHONE):
        context.user_data["phone_number"] = phone_number

        message = await update.effective_message.reply_text(
            ADD_NAME_TEXT.format(phone_number), reply_markup=buttons
        )

        message_control_dialog(context, message)

        return ADD_NAME_KEY

    message = await update.effective_message.reply_text(
        EXCEPT_ADD_NUMBER_TEXT, reply_markup=buttons
    )

    message_control_dialog(context, message)

    return ADD_NUMBER_KEY


async def show_add_email_page(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Ввод почты пользователя."""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "На страницу назад >> Ввод имени",
                    callback_data="/back_page",
                )
            ],
            [
                InlineKeyboardButton(
                    "Вернуться на главную страницу", callback_data="/back"
                )
            ],
        ]
    )

    user_name = update.message.text
    message_control_dialog(context, update.message)

    if is_valid_pattern(user_name, RE_PATTERN_NAME):
        context.user_data["user"] = user_name

        message = await update.message.reply_text(
            ADD_EMAIL_TEXT.format(user_name), reply_markup=buttons
        )
        message_control_dialog(context, message)

        return ADD_EMAIL_KEY

    message = await update.effective_message.reply_text(
        EXCEPT_ADD_NAME_TEXT, reply_markup=buttons
    )

    message_control_dialog(context, message)

    return ADD_NAME_KEY


async def end_add_contacts(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Конец ввода контактов."""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Повторно оставить контакты", callback_data="/add_contacts"
                )
            ],
            [
                InlineKeyboardButton(
                    "Вернуться на главную страницу", callback_data="/back"
                )
            ],
        ]
    )
    email = update.message.text

    await context.bot.delete_messages(
        update.effective_chat.id,
        message_control_dialog(context, update.message),
    )

    if is_valid_pattern(update.message.text, RE_PATTERN_EMAIL):
        context.user_data["email"] = email

        user_data = context.user_data

        phone_number = user_data.pop("phone_number")
        name = user_data.pop("user")
        email = user_data.pop("email")

        await update.message.reply_text(
            END_ADD_INFO_TEXT.format(name, phone_number, email),
            reply_markup=buttons,
        )

        current_user = await get_or_create_current_user(update.effective_user)

        async with AsyncSessionLocal() as session:
            user_repository.session = session

            user_data = context.user_data

            user_schema_update = UserSchemaUpdate(
                name=name, phone_number=phone_number, email=email
            )
            await user_repository.update(current_user, user_schema_update)

        return ConversationHandler.END

    await update.message.reply_text(
        EXCEPT_EMAIL_TEXT,
        reply_markup=buttons,
    )

    return ADD_EMAIL_KEY


STATES_COMMUNICATE = {
    ADD_NUMBER_KEY: [
        MessageHandler(filters.TEXT, show_add_name_page),
    ],
    ADD_NAME_KEY: [
        MessageHandler(filters.TEXT, show_add_email_page),
        CallbackQueryHandler(start_add_contacts, pattern="^/back_page$"),
    ],
    ADD_EMAIL_KEY: [
        MessageHandler(filters.TEXT, end_add_contacts),
        CallbackQueryHandler(show_add_name_page, pattern="^/back_page$"),
    ],
}

get_contacts_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_add_contacts, pattern="^/add_contacts$"),
    ],
    states=STATES_COMMUNICATE,
    fallbacks={},
)
