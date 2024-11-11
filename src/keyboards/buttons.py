from telegram import Update
from telegram.ext import ContextTypes

from handlers.category_selection import show_category_page
from handlers.contact_page import (
    get_contacts_handler,
    show_contacts_page,
    start_add_contacts,
)
from handlers.equipment_page import equipment_selection_handler
from handlers.help_page import show_help_page
from handlers.main_page import show_main_page
from handlers.maker_selection import (
    maker_selection_handler,
    show_maker_selection,
)
from handlers.model_selection import model_selection_handler
from handlers.properties_selection import (
    property_handler,
    show_properties_page,
)
from handlers.utils import handle_property_selection
from utils.update_page import decorator_delete_pre_msg
from utils.user import remove_user_convesate

story = []
mess_id = 0


def mess_id_check(update: Update) -> bool:
    """Сравнение id сообщения."""
    now_mess_id = update["callback_query"]["message"]["message_id"]
    global mess_id
    if mess_id < now_mess_id:
        mess_id = now_mess_id
        return True
    return False


async def handle_pagination(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: str
) -> None:
    """Обработка пагинации и навигации."""
    page = int(data.split(" ")[1])
    context.user_data['page'] = page
    category_id = context.user_data.get("category_id")
    property_ids = context.user_data.get("property_ids")
    maker_id = context.user_data.get("maker_id")

    if category_id and not property_ids:
        await property_handler(update, context)
    if category_id and property_ids and not maker_id:
        await maker_selection_handler(update, context)
    if category_id and property_ids and maker_id:
        await model_selection_handler(update, context)
    if not category_id:
        await show_category_page(update, context)


@decorator_delete_pre_msg
@remove_user_convesate(get_contacts_handler)
async def history_record(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Добавление событий в историю."""
    story.append((update, context))


@decorator_delete_pre_msg
@remove_user_convesate(get_contacts_handler)
async def step_back(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Кнопка На шаг назад."""
    story.pop(len(story) - 1)
    if len(story) == 0:
        await home_page(update, context)
    else:
        update = story[-1][0]
        context = story[-1][1]

        query = update.callback_query
        data = query.data

        if data == 'select_equipment':
            context.user_data["page"] = 0
            await show_category_page(update, context)

        if data.startswith("category_select_id"):
            context.user_data["page"] = 0
            category_id = int(data.split(" ")[1])
            context.user_data["category_id"] = category_id
            context.user_data["selected_properties"] = []
            await show_properties_page(update, context, category_id)

        if data.startswith("property_"):
            context.user_data["page"] = 0
            param_id = int(data.split("_")[1])
            await handle_property_selection(update, context, param_id)

        if data.startswith("maker_"):
            context.user_data["page"] = 0
            await maker_selection_handler(update, context)

        if data.startswith("model_"):
            context.user_data["page"] = 0
            maker_id = int(data.split("_")[1])
            await model_selection_handler(update, context, maker_id)

        if data.startswith("equipment_"):
            context.user_data["page"] = 0
            equipment_id = int(data.split("_")[1])
            await equipment_selection_handler(update, context, equipment_id)

        elif data.startswith("prev_page") or data.startswith("next_page"):
            await handle_pagination(update, context, data)


@decorator_delete_pre_msg
@remove_user_convesate(get_contacts_handler)
async def command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обработка сообщений."""
    global mess_id
    command = update["message"]["text"]
    mess_id_now = update["message"]["message_id"]
    if mess_id_now > mess_id:
        mess_id = mess_id_now
    if command == "/help":
        await help_page(update, context)
    if command == "/back":
        await home_page(update, context)
    if command == "/properties":
        await show_properties_page(update, context, category_id=1)
    if command == "/communicate":
        await show_contacts_page(update, context)
    if command == "/add_contacts":
        await start_add_contacts(update, context)


@decorator_delete_pre_msg
@remove_user_convesate(get_contacts_handler)
async def help_page(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Вернуться на главную."""
    story.clear()
    await show_help_page(update, context)
    context.user_data.clear()


@decorator_delete_pre_msg
@remove_user_convesate(get_contacts_handler)
async def home_page(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Вернуться на главную."""
    story.clear()
    await show_main_page(update, context)
    context.user_data.clear()


@decorator_delete_pre_msg
@remove_user_convesate(get_contacts_handler)
async def select_equipment(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Выбор категории."""
    if mess_id_check(update):
        await history_record(update, context)
        await show_category_page(update, context)


@decorator_delete_pre_msg
@remove_user_convesate(get_contacts_handler)
async def not_enough_properties(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отсутствие свойств."""
    category_id = context.user_data.get("category_id")
    property_ids = context.user_data.get("selected_properties", [])
    await show_maker_selection(update, context, category_id, property_ids)


@decorator_delete_pre_msg
@remove_user_convesate(get_contacts_handler)
async def enough_properties(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Выбор свойств."""
    if mess_id_check(update):
        category_id = context.user_data.get("category_id")
        await show_properties_page(update, context, category_id)


@decorator_delete_pre_msg
@remove_user_convesate(get_contacts_handler)
async def communicate(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Контакты."""
    if mess_id_check(update):
        await history_record(update, context)
        await show_contacts_page(update, context)


@decorator_delete_pre_msg
@remove_user_convesate(get_contacts_handler)
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка нажатий на кнопки."""
    query = update.callback_query
    data = query.data
    await query.answer()
    await history_record(update, context)
    if mess_id_check(update):
        if data.startswith("category_select_id"):
            context.user_data["page"] = 0
            category_id = int(data.split(" ")[1])
            context.user_data["category_id"] = category_id
            context.user_data["selected_properties"] = []
            await show_properties_page(update, context, category_id)

        if data.startswith("property_"):
            context.user_data["page"] = 0
            param_id = int(data.split("_")[1])
            await handle_property_selection(update, context, param_id)

        if data.startswith("maker_"):
            context.user_data["page"] = 0
            await maker_selection_handler(update, context)

        if data.startswith("model_"):
            context.user_data["page"] = 0
            maker_id = int(data.split("_")[1])
            await model_selection_handler(update, context, maker_id)

        if data.startswith("equipment_"):
            context.user_data["page"] = 0
            equipment_id = int(data.split("_")[1])
            await equipment_selection_handler(update, context, equipment_id)

        elif data.startswith("prev_page") or data.startswith("next_page"):
            await handle_pagination(update, context, data)
