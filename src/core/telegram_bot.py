import uvicorn
from fastadmin import fastapi_app as admin_panel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from admin_panel import AdminUser  # noqa
from core.config import settings  # noqa
from core.constants import BASE_DIR
from core.init_db import create_first_superuser
from handlers.contact_page import get_contacts_handler, show_contacts_page
from handlers.main_page import show_main_page
from keyboards.buttons import (
    button,
    command_handler,
    communicate,
    enough_properties,
    home_page,
    not_enough_properties,
    select_equipment,
    step_back,
)

app = FastAPI()
app.mount("/admin", admin_panel)
app.mount(
    "/media", StaticFiles(directory=str(BASE_DIR / "media")), name="media"
)


# Поменять т.к. он будет удален
@app.on_event("startup")
async def startup():
    """Create superuser."""
    await create_first_superuser()


async def start_bot() -> None:
    """Инициализация uvicorn."""
    webserver = uvicorn.Server(
        config=uvicorn.Config(app=app, host="0.0.0.0", port=8000)
    )
    application = ApplicationBuilder().token(settings.tg_token).build()

    start_command_handler = CommandHandler("start", show_main_page)
    application.add_handler(start_command_handler)

    communicate_command_handler = CommandHandler(
        "communicate", show_contacts_page
    )
    application.add_handler(communicate_command_handler)

    start_message_handler = MessageHandler(filters.COMMAND, command_handler)
    application.add_handler(start_message_handler)

    application.add_handler(get_contacts_handler)

    application.add_handler(CallbackQueryHandler(home_page, '/back'))
    application.add_handler(
        CallbackQueryHandler(select_equipment, 'select_equipment')
    )
    application.add_handler(
        CallbackQueryHandler(not_enough_properties, 'not_enough_properties')
    )
    application.add_handler(
        CallbackQueryHandler(enough_properties, 'enough_properties')
    )
    application.add_handler(CallbackQueryHandler(step_back, '/step_back'))
    application.add_handler(CallbackQueryHandler(communicate, '/communicate'))
    application.add_handler(CallbackQueryHandler(button))

    async with application:
        await application.start()
        await application.updater.start_polling(
            allowed_updates=Update.ALL_TYPES
        )
        await webserver.serve()
        await application.updater.stop()
        await application.stop()
