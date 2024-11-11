from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from models.equipment import Equipment
from models.helper import BaseModel

if TYPE_CHECKING:
    from models.equipment import Equipment


class Category(BaseModel):
    """Model Category."""

    equipment: Mapped['Equipment'] = relationship(
        back_populates="category", cascade="all,delete"
    )
