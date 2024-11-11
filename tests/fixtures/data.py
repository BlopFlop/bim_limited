import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import (
    Category,
    Equipment,
    EquipmentParameter,
    Maker,
    Parameter,
)


@pytest.fixture
async def category(session: AsyncSession):
    """Create category for tests."""
    db_obj = Category(
        id=1, name="Бытовой", description="Бытовая сплит-система"
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


@pytest.fixture
async def maker(session: AsyncSession):
    """Create maker for tests."""
    db_obj = Maker(
        id=1,
        name="MDV",
        description='Производитель "MDV"',
        logo="/media/mdv.jpeg",
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


@pytest.fixture
async def parameter_inverter(session: AsyncSession):
    """Create parameter_inverter for tests."""
    db_obj = Parameter(
        id=1, name="Инвертор", description="Инверторная сплит-система"
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


@pytest.fixture
async def parameter_otside(session: AsyncSession):
    """Create parameter_otside for tests."""
    db_obj = Parameter(id=2, name="Внешний", description="Внешний блок")
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


@pytest.fixture
async def equipment(session: AsyncSession):
    """Create equipment for tests."""
    db_obj = Equipment(
        id=1,
        name="INFINI NORDIC HEAT PUMP",
        description="INFINI NORDIC HEAT PUMP",
        maker_id=1,
        category_id=1,
        pdf_catalog="media/pdf/mdv_INFINI_NORDIC_HEAT_PUMP.pdf",
    )
    session.add(db_obj)
    await session.commit()
    param_1 = EquipmentParameter(id=1, equipment_id=1, parameter_id=1)
    param_2 = EquipmentParameter(id=2, equipment_id=1, parameter_id=2)
    await session.add_all((param_1, param_2))
    await session.commit()
    await session.refresh(db_obj)
    return db_obj
