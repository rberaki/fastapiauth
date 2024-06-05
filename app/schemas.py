from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email_address: EmailStr
    username: str


class UserEdit(UserBase):
    password: str


class User(UserBase):
    id: int
