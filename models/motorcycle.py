from pydantic import BaseModel, Field

class MotorcycleBase(BaseModel):
    plate: str
    brand: str
    model: str
    engine_displacement: int = Field(gt=0)
    year: int = Field(gt=0)
    mileage: int = Field(ge=0)
    user_id: str

class MotorcycleID(MotorcycleBase):
    id: int

class MotorcycleUpdate(BaseModel):
    plate: str
    brand: str
    model: str
    engine_displacement: int = Field(gt=0)
    year: int = Field(gt=0)
    mileage: int = Field(ge=0)
    user_id: str