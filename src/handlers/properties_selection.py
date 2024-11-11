from sqlalchemy import and_
from sqlalchemy.future import select
from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from core.db import AsyncSessionLocal
from handlers.maker_selection import show_maker_selection
from handlers.utils import get_category_name, paginate_buttons
from models import Equipment, Parameter


async def property_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обработка команды выбора свойств."""
    category_id = context.user_data.get("category_id", 1)
    await show_properties_page(
        update,
        context,
        category_id,
    )


async def show_properties_page(
    update: Update, context: ContextTypes.DEFAULT_TYPE, category_id: int
) -> None:
    """Отображение доступных свойств для выбранной категории."""
    selected_property_ids = context.user_data.get("selected_properties", [])

    async with AsyncSessionLocal() as session:
        if selected_property_ids:
            query = (
                select(Parameter)
                .join(Equipment.parameters)
                .filter(
                    and_(
                        Equipment.category_id == category_id,
                        Equipment.parameters.any(
                            Parameter.id.in_(selected_property_ids)
                        ),
                    )
                )
                .distinct()
            )
        else:
            query = (
                select(Parameter)
                .join(Equipment.parameters)
                .filter(Equipment.category_id == category_id)
                .distinct()
            )
        result = await session.execute(query)
        parameters = result.scalars().all()

    available_parameters = parameters

    if not available_parameters:
        category_id = context.user_data.get("category_id")
        property_ids = context.user_data.get("selected_properties", [])
        await show_maker_selection(update, context, category_id, property_ids)
        return

    buttons = [
        InlineKeyboardButton(param.name, callback_data=f"property_{param.id}")
        for param in available_parameters
    ]

    page = context.user_data.get('page', 0)
    markup = paginate_buttons(buttons, page)

    category_name = await get_category_name(session, category_id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f"Вы выбрали категорию: {category_name}\n"
            "Выберите свойства оборудования:"
        ),
        reply_markup=markup,
    )
