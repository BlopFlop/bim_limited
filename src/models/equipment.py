from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper import BaseModel

if TYPE_CHECKING:
    from models.category import Category
    from models.maker import Maker
    from models.parameter import Parameter


class Equipment(BaseModel):
    """Model Equipment."""

    equipment_picture: Mapped[str] = mapped_column(
        comment="picture link", nullable=True
    )
    maker_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('maker.id'),
        nullable=False,
        comment="relationship maker model",
    )
    maker: Mapped['Maker'] = relationship(
        back_populates="equipment",
        lazy="noload",
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("category.id"),
        nullable=False,
        comment="relationship category model",
    )
    category: Mapped['Category'] = relationship(
        back_populates="equipment", lazy="noload"
    )
    parameters: Mapped[list['Parameter']] = relationship(
        secondary="equipmentparameter",
        back_populates="equipments",
        lazy="noload",
    )
    pdf_catalog: Mapped[str] = mapped_column(
        unique=True, nullable=False, comment="pdf link"
    )
