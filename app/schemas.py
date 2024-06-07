from pydantic import BaseModel, EmailStr


class UsernameMixin(BaseModel):
    username: str


class UserPasswordMixin(BaseModel):
    password: str


class UserBaseMixin(UsernameMixin):
    firstname: str
    lastname: str
    email_address: EmailStr


class UserLogin(UsernameMixin, UserPasswordMixin):
    pass


class UserCreate(UserBaseMixin, UserPasswordMixin):
    pass


class UserUpdate(UserBaseMixin):
    password: str = None


class User(UserBaseMixin):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
