from sqlalchemy import Column, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, declared_attr

from core.base import Base


class BaseModel(Base):
    """Helper model."""

    __abstract__ = True

    name = Column(
        String(100),
        unique=True,
        nullable=False,
    )
    description = Column(
        Text,
        nullable=False,
    )

    def __repr__(self) -> str:
        return self.name


class PreBase:
    """Base model."""

    @declared_attr
    def __tablename__(cls):
        """Autocreate tablename."""
        return cls.__name__.lower()


class EquipmentParameterModel(Base):
    """Support model. It is support make many-to-many relation."""

    __tablename__ = "equipmentparameter"

    equipment_id: Mapped[int] = Column(
        ForeignKey("equipment.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="relationship equipment model",
    )
    parameter_id: Mapped[int] = Column(
        ForeignKey("parameter.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="relationship parameter model",
    )
    __table_args__ = (
        UniqueConstraint(
            "equipment_id",
            "parameter_id",
            name="idx_unique_equipment_parameter",
        ),
    )
