from typing import Optional, Generic

from fastapi_users import schemas, models
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    id: models.ID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    role_id: int
    name_first: str
    name_second: str
    username: str


class UserCreate(schemas.CreateUpdateDictModel, Generic[models.ID]):
    email: EmailStr
    password: str
    name_first: Optional[str]
    name_second: Optional[str]
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    email: EmailStr
    name_first: Optional[str]
    name_second: Optional[str]
    username: str
