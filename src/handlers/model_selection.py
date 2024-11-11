from sqlalchemy.future import select
from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from core.db import AsyncSessionLocal
from handlers.utils import (
    gel_maker_logo,
    get_category_name,
    get_parameter_name,
    paginate_buttons,
)
from models import Equipment, Parameter


async def model_selection_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE, maker_id: int
) -> None:
    """Обработка команды выбора моделей."""
    category_id = context.user_data.get("category_id")
    property_ids = context.user_data.get("selected_properties", [])
    await show_model_page(update, context, maker_id, category_id, property_ids)


async def show_model_page(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    maker_id: int,
    category_id: int,
    property_ids: list[int],
) -> None:
    """Отображение моделей."""
    async with AsyncSessionLocal() as session:

        if property_ids:
            query = (
                select(Equipment)
                .join(Equipment.parameters)
                .filter(
                    Equipment.maker_id == maker_id,
                    Equipment.category_id == category_id,
                    Parameter.id.in_(property_ids),
                )
                .distinct()
            )
        else:
            query = (
                select(Equipment)
                .filter(
                    Equipment.category_id == category_id,
                )
                .distinct()
            )

        result = await session.execute(query)
        models = result.scalars().all()

        if property_ids:
            parameter_names = [
                await get_parameter_name(session, pid)
                for pid in set(property_ids)
            ]
            parameter_names_text = ", ".join(parameter_names)
        else:
            parameter_names_text = "Нет"

        category_name = await get_category_name(session, category_id)

    buttons = [
        InlineKeyboardButton(model.name, callback_data=f"equipment_{model.id}")
        for model in models
    ]

    page = context.user_data.get('page', 0)
    markup = paginate_buttons(buttons, page)

    message_text = (
        f"Вы выбрали оборудование:\n"
        f"Категории: {category_name}\n"
        f"Свойства: {parameter_names_text}\n"
        f"Выберите интересующую вас модель:"
    )

    logo = await gel_maker_logo(session, maker_id)
    with open(logo, "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=markup,
        )
