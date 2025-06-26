from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserUpdatePartial(UserBase):
    pass


class User(UserBase):
    id: int

