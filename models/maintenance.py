from pydantic import BaseModel, Field

class MaintenanceBase(BaseModel):
    motorcycle_id: str
    maintenance_type: str
    date: str
    mileage: int = Field(ge=0)
    description: str
    cost: float = Field(ge=0)

class MaintenanceID(MaintenanceBase):
    id: int

class MaintenanceUpdate(BaseModel):
    motorcycle_id: str
    maintenance_type: str
    date: str
    mileage: int = Field(ge=0)
    description: str
    cost: float = Field(ge=0)