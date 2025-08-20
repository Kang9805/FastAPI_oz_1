# app/schemas/users.py
from enum import Enum
from pydantic import BaseModel
from pydantic.types import conint


class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'


class UserCreateRequest(BaseModel):
    username: str
    age: int
    gender: GenderEnum

class UserUpdateRequest(BaseModel):
    username: str | None = None
    age: int | None = None

class UserSearchParams(BaseModel):
    model_config = {"extra": "forbid"}

    username: str | None = None
    age: conint(gt=0) | None = None
    gender: GenderEnum | None = None

class Token(BaseModel):
    access_token: str
    token_type: str
