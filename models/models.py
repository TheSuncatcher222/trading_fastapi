from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class DegreeTypes(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeTypes


class Trades(BaseModel):
    """Model for Trades."""
    id: int
    user_id: int
    currency: str = Field(max_length=3)
    side: str
    price: float = Field(ge=0)
    amount: float


class Users(BaseModel):
    """Model for Users."""
    id: int
    role: str
    name: str
    degree: list[Degree] = []
