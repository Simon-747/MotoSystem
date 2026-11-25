from pydantic import BaseModel, Field as PydanticField
from sqlmodel import SQLModel, Field


class MotorcycleBase(SQLModel):
    plate: str
    brand: str
    model: str
    engine_displacement: int = PydanticField(gt=0)
    year: int = PydanticField(gt=0)
    mileage: int = PydanticField(ge=0)
    user_id: int


class MotorcycleID(MotorcycleBase, table=True):
    __tablename__ = "motorcycles"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")


class MotorcycleUpdate(BaseModel):
    plate: str
    brand: str
    model: str
    engine_displacement: int = PydanticField(gt=0)
    year: int = PydanticField(gt=0)
    mileage: int = PydanticField(ge=0)
    user_id: int
