from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField
from enums.maintenance_type import MaintenanceType


class MaintenanceBase(SQLModel):
    motorcycle_id: int
    maintenance_type: MaintenanceType
    date: str
    mileage: int = Field(ge=0)
    description: str
    cost: float = Field(ge=0)


class MaintenanceID(MaintenanceBase, table=True):
    __tablename__ = "maintenances"

    id: int | None = SQLField(default=None, primary_key=True)
    motorcycle_id: int = SQLField(foreign_key="motorcycles.id")


class MaintenanceUpdate(BaseModel):
    motorcycle_id: int
    maintenance_type: MaintenanceType
    date: str
    mileage: int = Field(ge=0)
    description: str
    cost: float = Field(ge=0)
