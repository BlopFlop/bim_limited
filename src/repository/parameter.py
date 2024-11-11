from sqlalchemy import select

from models.equipment import Equipment
from models.helper import EquipmentParameterModel
from models.parameter import Parameter
from repository.base import RepositoryBase


class ParameterRepository(RepositoryBase):
    """Parameter CRUD operations in current application."""

    async def get(
        self,
        obj_id: int,
    ):
        """Get one item model for id."""
        db_obj = await self.session.execute(
            select(self.model).where(self.model.id == obj_id).distinct()
        )
        result_obj: Parameter = db_obj.scalars().first()

        parameters = await self.session.execute(
            select(EquipmentParameterModel.parameter_id).filter(
                EquipmentParameterModel.equipment_id == obj_id
            )
        )

        db_equipments = await self.session.execute(
            select(Equipment)
            .filter(Equipment.id.in_(parameters.scalars().all()))
            .distinct()
        )

        result_obj.equipments = db_equipments.scalars().all()

        return result_obj


parameter_repository = ParameterRepository(Parameter)
