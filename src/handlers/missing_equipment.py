from typing import Union

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from models import Category, Maker
from text.messages import NO_EQUIPMENT_TEXT


async def show_no_equipment_page(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    item_object: Union[Maker, Category],
) -> None:
    """
    Универсальный фрейм отсутствия оборудования.

    :param update: объект Update
    :param context: объект CallbackContext
    :param item_object: категория (класса `Category`) или
        производитель (класса `Maker`)
    """
    if isinstance(item_object, Category):
        item_type = "категории"
    elif isinstance(item_object, Maker):
        item_type = "производителя"
    item_name = item_object.name

    text = NO_EQUIPMENT_TEXT.format(
        item_type=item_type,
        item_name=item_name,
    )
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Вернуться на главную страницу", callback_data="/back"
                )
            ],
        ]
    )
    await context.bot.send_message(
        update.effective_chat.id, text, reply_markup=buttons
    )
