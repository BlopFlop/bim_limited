from sqlalchemy.future import select
from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from core.db import AsyncSessionLocal
from handlers.utils import paginate_buttons
from models import Category
from text.messages import CATEGORY_PAGE_TEXT


async def show_category_page(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отображение категорий."""
    async with AsyncSessionLocal() as session:
        query = select(Category)
        result = await session.execute(query)
        categories = result.scalars().all()

    buttons = [
        InlineKeyboardButton(
            category.name, callback_data=f"category_select_id {category.id}"
        )
        for category in categories
    ]

    page = context.user_data.get('page', 0)
    markup = paginate_buttons(buttons, page)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CATEGORY_PAGE_TEXT,
        reply_markup=markup,
    )
