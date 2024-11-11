from typing import Final

MAIN_PAGE_TEXT: Final[str] = (
    "Здраствуйте вы в чат боте компании BIM Limited. "
    "Здесь вы можете подобрать необходимое для вас "
    'оборудование напрямую. Так же кнопка "Меню" '
    "позволит получить более полную информацию о "
    "функционале бота."
)
HELP_PAGE_TEXT: Final[str] = (
    "Данный бот поможет вам выбрать необходимое "
    "вам оборудование.\n"
    "Функции:\n"
    "/back - переход на главную страницу бота, здесь"
    "можно подобрать вам оборудование.\n"
    "/help - Команда для получения помощи о "
    "функционале бота.\n"
    "/communicate - Связь с консультантом."
)
CATEGORY_PAGE_TEXT: Final[str] = "Выберите категорию оборудования:"
PAGINATE_PREV_PAGE: Final[str] = "Предыдущая"
PAGINATE_NEXT_PAGE: Final[str] = "Следующая"
NO_EQUIPMENT_TEXT: Final[str] = (
    "Оборудования {item_type} {item_name} на данный момент нет."
)