from typing import Optional
from pydantic import BaseModel, Field


class PaymentPublic(BaseModel):
    id: int
    ticket_id: int
    amount: float
    
    class Config:
        from_attributes = True