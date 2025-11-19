from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import (
    Enum
)
from app.models.estimate import EstimateStatusEnum

class EstimateUpdate(BaseModel):
    id: int
    amount: int
    status: str
    ticket_id: int
    payment_id: int
    


class EstimatePublic(BaseModel):
    id: int
    ticket_id: int
    mechanic_id: int
    amount: float
    currency: str
    status: str

    class Config:
        from_attributes = True