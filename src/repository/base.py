from typing import Any

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session


class RepositoryBase:
    """Base CRUD operations in current application."""

    def __init__(
        self, model, session: AsyncSession = Depends(get_async_session)
    ):
        """."""
        self.model = model
        self.session = session

    async def get(
        self,
        obj_id: int,
    ):
        """Get one item model for id."""
        db_obj = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self):
        """Get all items model."""
        db_objs = await self.session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
    ):
        """Create item model for id."""
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
    ):
        """Update item model for id."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
    ):
        """Delete item model for id."""
        await self.session.delete(db_obj)
        await self.session.commit()
        return db_obj

    async def get_obj_for_field_arg(self, field: str, arg: Any, many: bool):
        """Get model for keyword argument."""
        db_obj = await self.session.execute(
            select(self.model).where(getattr(self.model, field) == arg)
        )
        if many:
            return db_obj.scalars().all()
        return db_obj.scalars().first()
