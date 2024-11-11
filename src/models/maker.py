from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper import BaseModel

if TYPE_CHECKING:
    from models.equipment import Equipment


class Maker(BaseModel):
    """Model Maker."""

    logo: Mapped[str] = mapped_column(
        unique=True, nullable=False, comment="logo link"
    )

    equipment: Mapped['Equipment'] = relationship(
        back_populates="maker", cascade="all,delete"
    )
