from pydantic import BaseModel, EmailStr
from enums.id_type import IdType


class UserBase(BaseModel):
    first_name: str
    last_name: str
    id_type: IdType
    document: str
    phone_number: str
    email: EmailStr

class UserID(UserBase):
    id: int

class UserUpdate(BaseModel):
    first_name: str
