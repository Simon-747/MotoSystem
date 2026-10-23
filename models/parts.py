from pydantic import BaseModel, Field


class PartsBase(BaseModel):
    name: str
    description: str
    category: str
    brand: str
    compatible_brands: list[str]
    price: float = Field(ge=0)
    stock: int = Field(ge=0)


class Parts(PartsBase):
    id: int


class PartsUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    brand: str | None = None
    compatible_brands: list[str] | None = None
    price: float | None = Field(default=None, ge=0)
    stock: int | None = Field(default=None, ge=0)
