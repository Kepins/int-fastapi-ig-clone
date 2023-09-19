from pydantic import BaseModel, SecretStr, EmailStr, ConfigDict


class UserBase(BaseModel):
    nickname: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    email: EmailStr
    password: SecretStr


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserLogin(BaseModel):
    nickname: str
    password: SecretStr
