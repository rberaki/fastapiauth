from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email_address: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str = None


class User(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
