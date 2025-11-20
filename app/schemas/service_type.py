from typing import Optional
from pydantic import BaseModel, Field


class ServiceTypePublic(BaseModel):
    id: int
    category_id: int
    name: str
    description: str
    
    class Config:
        from_attributes = True