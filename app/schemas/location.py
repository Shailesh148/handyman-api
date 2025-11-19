from typing import Optional
from pydantic import BaseModel, Field


class LocationCreate(BaseModel):
    label: Optional[str] = Field(None, max_length=100)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_primary: bool = False
    user_id: int

class LocationPublic(BaseModel):
    id: int
    label: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    is_primary: bool

    class Config:
        from_attributes = True
