import re

from fastadmin.api.exceptions import AdminApiException

from core.db import AsyncSessionLocal
from repository.base import RepositoryBase


def is_valid_pattern(item: str, pattern: str) -> bool:
    """Validate string for re pattern."""
    return bool(re.findall(pattern, item))


async def check_unique_field(
    repository: RepositoryBase, id: int, field: str, arg: str
) -> None | AdminApiException:
    """Check unique field obj in db."""
    async with AsyncSessionLocal() as session:
        repository.session = session

        obj = await repository.get_obj_for_field_arg(
            field=field, arg=arg, many=False
        )
        if obj and id and (obj.id == id):
            obj = None

    if obj:
        except_message: str = (
            f"Поле {field} со значением {arg} уже существует."
        )
        raise AdminApiException(400, except_message)
