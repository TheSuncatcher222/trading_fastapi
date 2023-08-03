from pydantic import BaseModel, Field


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
