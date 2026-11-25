from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field
from enums.id_type import IdType


class UserBase(SQLModel):
    first_name: str
    last_name: str
    id_type: IdType
    document: str
    phone_number: str
    email: EmailStr
    image: str | None = None


class UserID(UserBase, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    id_type: IdType | None = None
    document: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    image: str | None = None
