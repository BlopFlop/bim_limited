import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from fastadmin.settings import settings as fastadmin_settings
from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings

from core.constants import (
    ENV_PATH,
    LOG_DIR,
    LOG_FILE,
    LOG_FORMAT,
    LOGO_PNG_PATH,
)


class Settings(BaseSettings):
    """Settings for current project."""

    name_company: str = "SomeCompany"

    tg_token: str = 'tg_token'

    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    db_host: str = Field(alias="POSTGRES_SERVER")
    db_port: str = Field(alias="POSTGRES_PORT")

    secret: str = Field(alias="SECRET")
    first_superuser_email: Optional[EmailStr] = Field(
        alias="FIRST_SUPERUSER_EMAIL"
    )
    first_superuser_password: Optional[str] = Field(
        alias="FIRST_SUPERUSER_PASSWORD"
    )

    admin_user_model: str = Field(alias="ADMIN_USER_MODEL")
    admin_user_model_username_field: str = Field(
        alias="ADMIN_USER_MODEL_USERNAME_FIELD"
    )
    admin_secret_key: str = Field(alias="ADMIN_SECRET_KEY")

    consultate_number: str = Field(alias="CONSULTATE_NUMBER")
    consultate_url: str = Field(alias="CONSULTATE_URL")
    consultate_mail: str = Field(alias="CONSULTATE_MAIL")
    consultate_telegram: str = Field(alias="CONSULTATE_TELEGRAM")

    drectory_logo_maker: str = Field(alias="DIRECTORY_LOGO_MAKER")
    drectory_image_equipment: str = Field(alias="DIRECTORY_IMAGE_EQUIPMENT")
    drectory_pdf: str = Field(alias="DIRECTORY_PDF")

    @property
    def database_url(self) -> str:
        """Return database url from .env ."""
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.postgres_user,
            self.postgres_password,
            self.db_host,
            self.db_port,
            self.postgres_db,
        )

    class Config:
        """Config for the meta class in current settings."""

        env_file = ENV_PATH
        extra = "ignore"


def configure_logging() -> None:
    """Configure logging from this project."""
    LOG_DIR.mkdir(exist_ok=True)
    rotating_handler: RotatingFileHandler = RotatingFileHandler(
        LOG_FILE, maxBytes=10**6, backupCount=5
    )
    rotating_handler.setFormatter(LOG_FORMAT)
    project_logger = logging.getLogger("bim_web_app_logging")
    project_logger.setLevel(logging.INFO)
    project_logger.addHandler(rotating_handler)
    project_logger.addHandler(logging.StreamHandler())


settings = Settings()

fastadmin_settings.ADMIN_SECRET_KEY = settings.admin_secret_key
fastadmin_settings.ADMIN_USER_MODEL = settings.admin_user_model
fastadmin_settings.ADMIN_USER_MODEL_USERNAME_FIELD = (
    settings.admin_user_model_username_field
)
fastadmin_settings.ADMIN_SITE_NAME = "BIM Limited"
fastadmin_settings.ADMIN_PRIMARY_COLOR = "#30324e"
fastadmin_settings.ADMIN_SITE_FAVICON = LOGO_PNG_PATH
fastadmin_settings.ADMIN_SITE_HEADER_LOGO = LOGO_PNG_PATH
fastadmin_settings.ADMIN_SITE_SIGN_IN_LOGO = LOGO_PNG_PATH

configure_logging()
