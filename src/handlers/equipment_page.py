from sqlalchemy.future import select
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from core.config import settings
from core.db import AsyncSessionLocal
from handlers.utils import (
    gel_maker_logo,
    get_category_name,
    get_parameter_name,
    show_back_button,
    show_main_page_button,
)
from models import Equipment


async def equipment_selection_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE, equipment_id: int
) -> None:
    """Обработка команды выбора оборудования."""
    category_id = context.user_data.get("category_id")
    property_ids = context.user_data.get("selected_properties", [])
    await show_equipment_page(
        update, context, equipment_id, category_id, property_ids
    )


async def show_equipment_page(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    equipment_id: int,
    category_id: int,
    property_ids: list[int],
) -> None:
    """Отображение обарудования."""
    async with AsyncSessionLocal() as session:

        query = select(Equipment).filter_by(id=equipment_id)
        result = await session.execute(query)
        equipment = result.scalar()

        parameter_names = [
            await get_parameter_name(session, pid) for pid in set(property_ids)
        ]
        parameter_names_text = ", ".join(parameter_names)

        category_name = await get_category_name(session, category_id)

    message_text = (
        f"Вы выбрали оборудование:\n"
        f"Категории: {category_name}\n"
        f"Свойства: {parameter_names_text}\n"
        f"Отличный выбор. Ждем вашего звонка\n"
        f"Наименование: {equipment.name}\n"
        f"Описание: {equipment.description}\n"
        f"\n"
        f"А так же вы можете связаться с нами:\n"
        f"WhatsApp: {settings.consultate_number}\n"
        f"Mail: {settings.consultate_mail}\n"
        f"\n"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Сайт", url=settings.consultate_url),
                InlineKeyboardButton(
                    "Телеграм", url=settings.consultate_telegram
                ),
            ],
            [show_back_button()],
            [show_main_page_button()],
        ]
    )

    if equipment.equipment_picture is not None:
        logo = equipment.equipment_picture
    else:
        logo = await gel_maker_logo(session, int(equipment.maker_id))

    with open(
        equipment.pdf_catalog,
        "rb",
    ) as document:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=document,
        )

    with open(logo, "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=message_text,
            parse_mode="HTML",
            reply_markup=buttons,
        )
