from pydantic import BaseModel, Field as PydanticField
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON


class PartsBase(SQLModel):
    name: str
    description: str
    category: str
    brand: str
    compatible_brands: list[str]
    price: float = PydanticField(ge=0)
    stock: int = PydanticField(ge=0)


class Parts(PartsBase, table=True):
    __tablename__ = "parts"

    id: int | None = Field(default=None, primary_key=True)
    compatible_brands: list[str] = Field(
        sa_column=Column(JSON, nullable=False)
    )
    is_active: bool = Field(default=True)


class PartsUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    brand: str | None = None
    compatible_brands: list[str] | None = None
    price: float | None = PydanticField(default=None, ge=0)
    stock: int | None = PydanticField(default=None, ge=0)
