from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

LOG_DIR: Final[Path] = BASE_DIR / "logs"
LOG_FILE: Final[Path] = LOG_DIR / "bim_web_app_logging.log"
DATE_FORMAT: Final[str] = "%Y-%m-%d"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'

ENV_PATH: Final[Path] = BASE_DIR.parent / r"infra//.env"

STATIC_PATH: Final[Path] = BASE_DIR / "static"
LOGO_PNG_PATH: Final[Path] = STATIC_PATH / "logo.png"


RE_PATTERN_NUMBER_PHONE: Final[str] = (
    r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
)
RE_PATTERN_NAME: Final[str] = r"^[а-яА-Яa-zA-Z0-9]+$"
RE_PATTERN_EMAIL: Final[str] = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
