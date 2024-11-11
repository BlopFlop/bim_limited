from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from models.helper import BaseModel

if TYPE_CHECKING:
    from models.equipment import Equipment


class Parameter(BaseModel):
    """Model Parametr."""

    equipments: Mapped[list['Equipment']] = relationship(
        secondary="equipmentparameter",
        back_populates="parameters",
        lazy="noload",
    )
