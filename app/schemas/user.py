from pydantic import BaseModel, SecretStr, EmailStr, ConfigDict, Extra


class UserBase(BaseModel, extra=Extra.forbid):
    first_name: str
    last_name: str


class UserCreate(UserBase):
    nickname: str
    email: EmailStr
    password: SecretStr


class UserUpdate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nickname: str


class UserLogin(BaseModel, extra=Extra.forbid):
    nickname: str
    password: SecretStr


class UserResetPassword(BaseModel, extra=Extra.forbid):
    old_password: SecretStr
    new_password: SecretStr
