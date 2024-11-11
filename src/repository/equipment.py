from sqlalchemy import select

from models.equipment import Equipment
from models.helper import EquipmentParameterModel
from models.parameter import Parameter
from repository.base import RepositoryBase


class EquipmentRepository(RepositoryBase):
    """Equipment CRUD operations in current application."""

    async def get(
        self,
        obj_id: int,
    ):
        """Get one item model for id."""
        db_obj = await self.session.execute(
            select(self.model).where(self.model.id == obj_id).distinct()
        )
        result_obj: Equipment = db_obj.scalars().first()

        equipments = await self.session.execute(
            select(EquipmentParameterModel.equipment_id).filter(
                EquipmentParameterModel.parameter_id == obj_id
            )
        )

        db_parameters = await self.session.execute(
            select(Parameter).filter(
                Parameter.id.in_(equipments.scalars().all())
            )
        )

        result_obj.parameters = db_parameters.scalars().all()

        return result_obj


equipment_repository = EquipmentRepository(Equipment)
