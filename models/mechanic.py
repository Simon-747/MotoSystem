from pydantic import BaseModel, EmailStr

class MechanicBase(BaseModel):
    first_name: str
    last_name: str
    document: str
    phone_number: str
    email: EmailStr

class Mechanic(MechanicBase):
    id: int

class MechanicUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    document: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
