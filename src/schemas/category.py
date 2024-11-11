from typing import Optional

from pydantic import BaseModel, Field


class CategorySchemaBase(BaseModel):
    """Base category schema."""

    name: str = Field(title="name", description="Имя категории")

    description: str = Field(
        title="description", description="Описание категории"
    )


class CategorySchemaCreate(BaseModel):
    """Create category schema."""

    pass


class CategorySchemaUpdate(BaseModel):
    """Update category schema."""

    name: Optional[str] = Field(
        None, title="name", description="Имя категории"
    )

    description: Optional[str] = Field(
        None, title="description", description="Описание категории"
    )


class CategorySchemaDB(CategorySchemaBase):
    """Result category schema."""

    id: int = Field(
        title="Id Category in db",
        description="Id Категории в базе данных.",
    )

    class Config:
        """Config for this schemas."""

        orm_mode: bool = True
