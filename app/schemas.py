from pydantic import BaseModel, EmailStr


class Username(BaseModel):
    username: str


class UserBase(Username, BaseModel):
    firstname: str
    lastname: str
    email_address: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str = None


class User(UserBase):
    id: int


class UserLogin(Username, BaseModel):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
