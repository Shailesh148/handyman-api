from pydantic import BaseModel, Field
from typing import Optional, List
from .inventory import InventoryPublic


class GarageCreate(BaseModel):
	name: str = Field(..., max_length=200)
	phone: Optional[str] = Field(None, max_length=20)
	email: Optional[str] = Field(None, max_length=255)
	address: Optional[str] = None
	latitude: Optional[float] = None
	longitude: Optional[float] = None
	type: str


class GaragePublic(BaseModel):
	id: int
	name: str
	phone: Optional[str]
	email: Optional[str]
	address: Optional[str]
	latitude: Optional[float]
	longitude: Optional[float]
	inventory: Optional[List[InventoryPublic]] = None
	type: str
	class Config:
		from_attributes = True
  
class AllGaragesPublic(BaseModel):
	id: int
	name: str
	phone: Optional[str]
	email: Optional[str]
	address: Optional[str]
	latitude: Optional[float]
	longitude: Optional[float]
	type: str
	class Config:
		from_attributes = True




class GarageUserAssign(BaseModel):
	user_id: int
	role: Optional[str] = None

