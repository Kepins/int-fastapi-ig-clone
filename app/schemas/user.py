from pydantic import BaseModel, SecretStr, EmailStr, ConfigDict


class UserBase(BaseModel):
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


class UserLogin(BaseModel):
    nickname: str
    password: SecretStr
