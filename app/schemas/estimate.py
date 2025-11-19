from typing import Optional
from pydantic import BaseModel, Field


class EstimatePublic(BaseModel):
    id: int
    ticket_id: int
    mechanic_id: int

    class Config:
        from_attributes = True