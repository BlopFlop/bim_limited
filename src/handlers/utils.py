from math import ceil

from sqlalchemy.future import select
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from models import Category, Maker, Parameter
from text.messages import PAGINATE_NEXT_PAGE, PAGINATE_PREV_PAGE


def show_back_button() -> InlineKeyboardButton:
    """Показать кнопку назад."""
    return InlineKeyboardButton("На шаг назад", callback_data='/step_back')


def show_main_page_button() -> InlineKeyboardButton:
    """Показать кнопку возврата на фрейм main."""
    return InlineKeyboardButton("Вернуться на главную", callback_data='/back')


def paginate_buttons(buttons, page: int) -> InlineKeyboardMarkup:
    """Пагинация кнопок с добавлением навигационных кнопок."""
    items_per_page = 4
    total_pages = ceil(len(buttons) / items_per_page)
    start_index = page * items_per_page
    end_index = start_index + items_per_page
    paginated_buttons = buttons[start_index:end_index]

    structured_buttons = []
    for i in range(0, len(paginated_buttons), 2):
        start_index = i
        end_index = i + 2
        structured_buttons.append(paginated_buttons[start_index:end_index])

    navigation_buttons = [
        (
            InlineKeyboardButton(
                PAGINATE_PREV_PAGE,
                callback_data=f'prev_page {max(0, page - 1)}',
            )
            if page > 0
            else InlineKeyboardButton(
                PAGINATE_PREV_PAGE,
                callback_data='no_action',
            )
        ),
        InlineKeyboardButton(
            f"{page + 1} Стр из {total_pages}", callback_data='no_action'
        ),
        (
            InlineKeyboardButton(
                PAGINATE_NEXT_PAGE,
                callback_data=f'next_page {min(total_pages - 1, page + 1)}',
            )
            if page < total_pages - 1
            else InlineKeyboardButton(
                PAGINATE_NEXT_PAGE, callback_data='no_action'
            )
        ),
    ]

    back_button = [show_back_button()]

    main_page_button = [show_main_page_button()]

    if any(btn.callback_data != 'no_action' for btn in navigation_buttons):
        structured_buttons.append(navigation_buttons)
    structured_buttons.append(back_button)
    structured_buttons.append(main_page_button)

    return InlineKeyboardMarkup(structured_buttons)


async def get_category_name(session, category_id: int) -> str:
    """Получение имени категории по ID."""
    query = select(Category.name).filter_by(id=category_id)
    result = await session.execute(query)
    return result.scalar()


async def get_parameter_name(session, parameter_id: int) -> str:
    """Получение имени параметра по ID."""
    query = select(Parameter.name).filter_by(id=parameter_id)
    result = await session.execute(query)
    return result.scalar()


def create_property_query_buttons() -> InlineKeyboardMarkup:
    """Создание кнопок для запроса дополнительных свойств."""
    buttons = [
        InlineKeyboardButton("Да", callback_data="enough_properties"),
        InlineKeyboardButton("Нет", callback_data="not_enough_properties"),
    ]

    return InlineKeyboardMarkup([buttons])


async def handle_property_selection(
    update: Update, context: ContextTypes.DEFAULT_TYPE, param_id: int
) -> None:
    """Обработка выбора свойства и запрос о дополнительных свойствах."""
    selected_properties = context.user_data.get("selected_properties", [])
    selected_properties.append(param_id)
    context.user_data["selected_properties"] = selected_properties

    markup = create_property_query_buttons()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Есть ли еще свойство? Нажмите 'Да', "
            "если хотите выбрать еще одно свойство, "
            "или 'Нет', если выбрали все."
        ),
        reply_markup=markup,
    )


async def gel_maker_logo(session, maker_id: int):
    """Обработка логотипа производителя."""
    query = select(Maker).filter_by(id=maker_id)
    result = await session.execute(query)
    return result.scalar().logo
