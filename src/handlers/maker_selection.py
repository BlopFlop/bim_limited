from sqlalchemy.future import select
from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from core.db import AsyncSessionLocal
from handlers.missing_equipment import show_no_equipment_page
from handlers.utils import (
    get_category_name,
    get_parameter_name,
    paginate_buttons,
)
from models import Category, Equipment, Maker, Parameter


async def maker_selection_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обработка команды выбора производителей."""
    category_id = context.user_data.get("category_id")
    property_ids = context.user_data.get("selected_properties", [])
    await show_maker_selection(update, context, category_id, property_ids)


async def show_maker_selection(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    category_id: int,
    property_ids: list[int],
) -> None:
    """Отображение производителей для выбранной категории и свойств."""
    # вынести общую часть за асинк
    async with AsyncSessionLocal() as session:
        if property_ids:
            query = (
                select(Maker)
                .join(Equipment.maker)
                .join(Equipment.parameters)
                .filter(
                    Equipment.category_id == category_id,
                    Parameter.id.in_(property_ids),
                )
                .distinct()
            )
        else:
            query = (
                select(Maker)
                .join(Equipment.maker)
                .filter(
                    Equipment.category_id == category_id,
                )
                .distinct()
            )
        result = await session.execute(query)
        makers = result.scalars().all()

        if property_ids:
            parameter_names = [
                await get_parameter_name(session, pid)
                for pid in set(property_ids)
            ]
            parameter_names_text = ", ".join(parameter_names)
        else:
            parameter_names_text = "Нет"

        category_name = await get_category_name(session, category_id)

    if not makers:
        await show_no_equipment_page(
            update, context, Category(name=category_name)
        )
        return

    buttons = [
        InlineKeyboardButton(maker.name, callback_data=f"model_{maker.id}")
        for maker in makers
    ]

    page = context.user_data.get('page', 0)
    markup = paginate_buttons(buttons, page)

    message_text = (
        f"Вы выбрали оборудование:\n"
        f"Категория: {category_name}\n"
        f"Свойства: {parameter_names_text}\n"
        f"Выберите производителя:"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text,
        reply_markup=markup,
    )
