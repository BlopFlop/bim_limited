from pathlib import Path
from uuid import UUID

from fastadmin import SqlAlchemyModelAdmin, WidgetType, display, register
from fastadmin.api.exceptions import AdminApiException
from sqlalchemy import select

from core.administration_user import UserManager, get_user_db, password_helper
from core.config import settings
from core.db import AsyncSessionLocal
from models import (
    AdministrationUser,
    Category,
    Equipment,
    Maker,
    Parameter,
    User,
)
from repository import (
    administration_user_repository,
    category_repository,
    equipment_repository,
    maker_repository,
    parameter_repository,
    user_repository,
)
from utils.file_worker import DataBase64, delete_file
from utils.validations import check_unique_field


@register(AdministrationUser, sqlalchemy_sessionmaker=AsyncSessionLocal)
class AdminUser(SqlAlchemyModelAdmin):
    """Register AdminUser model."""

    verbose_name = "Администратор"
    verbose_name_plural = "Администраторы"

    list_display = (
        "id",
        "email",
        "is_superuser",
        "is_active",
    )
    list_display_links = ("id",)
    list_filter = ("id", "email", "is_superuser", "is_active")
    search_fields = ("email",)

    fieldsets = (
        ("Logopass", {"fields": ("email", "hashed_password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                )
            },
        ),
    )
    formfield_overrides = {
        "email": (WidgetType.EmailInput, {"required": True}),
        "hashed_password": (WidgetType.PasswordInput, {"required": True}),
    }

    async def authenticate(self, email: str, password: str) -> None:
        """View the User panel."""
        sessionmaker = self.get_sessionmaker()
        async with sessionmaker() as session:
            query = select(AdministrationUser).filter_by(
                email=email, is_superuser=True
            )
            result = await session.scalars(query)
            user: AdministrationUser = result.first()

            user_db = get_user_db(session)
            user_manager = UserManager(user_db, password_helper)

            if not user:
                return None
            if not user_manager.password_helper.verify_and_update(
                password, user.hashed_password
            )[0]:
                return None
            return user.id

    async def save_model(self, id: int, payload: dict | None) -> dict | None:
        """Save method for processing Admin password."""
        await check_unique_field(
            administration_user_repository,
            id=id,
            field='email',
            arg=payload['email'],
        )

        if "$argon2id" not in payload['hashed_password']:
            password = password_helper.hash(payload['hashed_password'])
            payload['hashed_password'] = password
        return await super().save_model(id, payload)


@register(Category, sqlalchemy_sessionmaker=AsyncSessionLocal)
class AdminModelCategory(SqlAlchemyModelAdmin):
    """Register model Category."""

    list_display = ("id", "name", "description")

    list_display_widths: dict[str, str] = {
        "id": "30px",
        "name": "100px",
        "description": "150px",
    }

    verbose_name = "Категория"
    verbose_name_plural = "Категории"

    async def orm_delete_obj(self, id: UUID | int) -> None:
        """Delete currnet object and delete relation files."""
        sessionmaker = self.get_sessionmaker()
        async with sessionmaker() as session:
            category_repository.session = session
            equipment_repository.session = session

            obj: Category = await session.get(self.model_cls, id)

            equipments: list[Equipment] = (
                await equipment_repository.get_obj_for_field_arg(
                    field="category_id", arg=obj.id, many=True
                )
            )
            for equipment in equipments:
                picture_path = Path(equipment.equipment_picture)
                pdf_path = Path(equipment.pdf_catalog)

                delete_file(picture_path)
                delete_file(pdf_path)

            await category_repository.remove(obj)

    async def save_model(
        self, id: UUID | int | None, payload: dict
    ) -> dict | None:
        """Save method for Category model."""
        await check_unique_field(
            category_repository, id=id, field="name", arg=payload["name"]
        )

        return await super().save_model(id, payload)


@register(Maker, sqlalchemy_sessionmaker=AsyncSessionLocal)
class AdminModelMaker(SqlAlchemyModelAdmin):
    """Register model Maker."""

    list_display = ("id", "name", "description")
    list_display_widths: dict[str, str] = {
        "id": "30px",
        "name": "100px",
        "description": "150px",
    }

    formfield_overrides = {"logo": (WidgetType.Upload, {"required": True})}

    verbose_name = "Производитель"
    verbose_name_plural = "Производители"

    async def orm_delete_obj(self, id: UUID | int) -> None:
        """Delete currnet object and delete relation files."""
        sessionmaker = self.get_sessionmaker()
        async with sessionmaker() as session:
            maker_repository.session = session
            equipment_repository.session = session

            obj: Maker = await session.get(self.model_cls, id)

            logo_file_path = Path(obj.logo)

            equipments: list[Equipment] = (
                await equipment_repository.get_obj_for_field_arg(
                    field="maker_id", arg=obj.id, many=True
                )
            )
            for equipment in equipments:
                picture_path = Path(equipment.equipment_picture)
                pdf_path = Path(equipment.pdf_catalog)

                delete_file(picture_path)
                delete_file(pdf_path)

            await maker_repository.remove(obj)

            delete_file(logo_file_path)

    async def save_model(self, id: int, payload: dict | None) -> dict | None:
        """Save method for Maker model."""
        image_name = payload['name']

        await check_unique_field(
            maker_repository, id=id, field="name", arg=image_name
        )

        logo_image = payload['logo']

        if DataBase64.BASE64 in logo_image:
            base64_obj = DataBase64(logo_image)

            if "image" not in base64_obj.type_data:
                except_message = (
                    "В поле logo необходимо загрузить изображение"
                    f" а не файл с расширением {base64_obj.ext}."
                )
                raise AdminApiException(400, except_message)

            logo_image = base64_obj.save_file(
                image_name, Path(settings.drectory_logo_maker)
            )

        fields = self.get_model_fields_with_widget_types(
            with_m2m=False, with_upload=False
        )
        fields_payload = {
            field.column_name: self.deserialize_value(
                field, payload[field.name]
            )
            for field in fields
            if field.name in payload
        }

        fields_payload["logo"] = str(logo_image)
        obj = await self.orm_save_obj(id, fields_payload)
        if not obj:
            return None
        return await self.serialize_obj(obj)


@register(Parameter, sqlalchemy_sessionmaker=AsyncSessionLocal)
class AdminModelParameter(SqlAlchemyModelAdmin):
    """Register Parameter model."""

    list_display = ("id", "name", "description")
    list_display_widths: dict[str, str] = {
        "id": "30px",
        "name": "100px",
        "description": "150px",
        "equipments": "100px",
    }

    verbose_name = "Параметр оборудования"
    verbose_name_plural = "Параметры оборудования"

    async def save_model(self, id: int, payload: dict | None) -> dict | None:
        """Save method for Parameter model."""
        await check_unique_field(
            parameter_repository, id=id, field="name", arg=payload["name"]
        )

        if payload.get('equipments') is not None:
            payload["equipments"] = [
                int(equipment) for equipment in payload["equipments"]
            ]
        return await super().save_model(id, payload)


@register(Equipment, sqlalchemy_sessionmaker=AsyncSessionLocal)
class AdminModelEquipment(SqlAlchemyModelAdmin):
    """Register Equipment model."""

    list_display = (
        "id",
        "name",
        "description",
        "maker_name",
        "category_name",
        "parameters",
    )
    list_display_widths: dict[str, str] = {
        "id": "30px",
        "name": "100px",
        "description": "150px",
        "maker_name": "100px",
        "category_name": "100px",
    }

    list_display_links = "id"
    list_select_related = ("category", "maker", "parameters")
    formfield_overrides = {
        "equipment_picture": (WidgetType.Upload, {"required": True}),
        "pdf_catalog": (WidgetType.Upload, {"required": True}),
    }

    verbose_name = "Оборудование"
    verbose_name_plural = "Оборудованиe"

    @display
    async def category_name(self, obj):
        """Display category_name."""
        return str(obj.category)

    @display
    async def maker_name(self, obj):
        """Display maker_name."""
        return str(obj.maker)

    async def orm_delete_obj(self, id: UUID | int) -> None:
        """Delete currnet object and delete relation files."""
        sessionmaker = self.get_sessionmaker()
        async with sessionmaker() as session:
            equipment_repository.session = session

            obj: Equipment = await equipment_repository.get(id)

            picture_file_path = Path(obj.equipment_picture)
            pdf_picture_file_path = Path(obj.pdf_catalog)

            await equipment_repository.remove(obj)

            delete_file(pdf_picture_file_path)
            delete_file(picture_file_path)

    async def save_model(self, id: int, payload: dict | None) -> dict | None:
        """Save method for Equipment model."""
        await check_unique_field(
            equipment_repository, id=id, field="name", arg=payload["name"]
        )

        payload["maker"] = int(payload["maker"])

        payload["category"] = int(payload["category"])

        if payload.get('parameters'):
            payload["parameters"] = [
                int(parameter) for parameter in payload["parameters"]
            ]

        name_for_files = payload['name']

        equipment_picture: str = payload.get('equipment_picture', '')
        pdf_equipment: str = payload.get('pdf_catalog', '')

        if DataBase64.BASE64 in equipment_picture:
            base64_obj = DataBase64(equipment_picture)

            if "image" not in base64_obj.type_data:
                except_message = (
                    "В поле equipment_picture необходимо загрузить изображение"
                    f" а не файл с расширением {base64_obj.ext}."
                )
                raise AdminApiException(400, except_message)

            equipment_picture = base64_obj.save_file(
                name_for_files, Path(settings.drectory_image_equipment)
            )

        if DataBase64.BASE64 in pdf_equipment:
            base64_obj = DataBase64(pdf_equipment)

            if (
                "application" not in base64_obj.type_data
                and "pdf" not in base64_obj.ext
            ):
                except_message = (
                    "В поле pdf_catalog необходимо загрузить"
                    f" pdf а не файл с расширением {base64_obj.ext}."
                )
                raise AdminApiException(400, except_message)

            pdf_equipment = base64_obj.save_file(
                name_for_files, Path(settings.drectory_pdf)
            )

        fields = self.get_model_fields_with_widget_types(
            with_m2m=False, with_upload=False
        )
        m2m_fields = self.get_model_fields_with_widget_types(with_m2m=True)
        fields_payload = {
            field.column_name: self.deserialize_value(
                field, payload[field.name]
            )
            for field in fields
            if field.name in payload
        }
        fields_payload["equipment_picture"] = str(equipment_picture)
        fields_payload["pdf_catalog"] = str(pdf_equipment)
        obj = await self.orm_save_obj(id, fields_payload)

        if not obj:
            return None

        for m2m_field in m2m_fields:
            if m2m_field.name in payload:
                await self.orm_save_m2m_ids(
                    obj, m2m_field.column_name, payload[m2m_field.name]
                )
        return await self.serialize_obj(obj)


@register(User, sqlalchemy_sessionmaker=AsyncSessionLocal)
class AdminModelTgUser(SqlAlchemyModelAdmin):
    """Save method for User model."""

    verbose_name = "Телеграм пользователь"
    verbose_name_plural = "Телеграм пользователи"

    list_display = (
        "id",
        "tg_username",
        "tg_chat_id",
        "name",
        "phone_number",
        "email",
    )

    async def save_model(self, id: int, payload: dict | None) -> dict | None:
        """Save method for Parameter model."""
        await check_unique_field(
            user_repository,
            id=id,
            field="tg_username",
            arg=payload["tg_username"],
        )
        payload["tg_chat_id"] = int(payload["tg_chat_id"])
        await check_unique_field(
            user_repository,
            id=id,
            field="tg_chat_id",
            arg=payload["tg_chat_id"],
        )

        return await super().save_model(id, payload)
