from pydantic import BaseModel, Field


class Trade(BaseModel):
    """Model for Trades."""
    id: int
    user_id: int
    currency: str = Field(max_length=3)
    side: str
    price: float = Field(ge=0)
    amount: float
