import enum
from pydantic import BaseModel, Field
from typing import Optional


class ItemType(str, enum.Enum):
	TOOL = "TOOL"
	PART = "PART"


class ItemCreate(BaseModel):
	name: str = Field(..., max_length=150)
	item_type: ItemType
	unit: Optional[str] = Field(None, max_length=50)


class ItemPublic(BaseModel):
	id: int
	name: str
	item_type: ItemType
	unit: Optional[str]

	class Config:
		from_attributes = True




