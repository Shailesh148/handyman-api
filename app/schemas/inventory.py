import enum
from typing import Optional
from pydantic import BaseModel, Field
from .item import ItemPublic


class InventoryCreate(BaseModel):
	item_id: int
	garage_id: Optional[int] = None
	operator_user_id: Optional[int] = None
	minimum_quantity: int = 0
	maximum_quantity: int = 0
	quantity: int = 0


class InventoryPublic(BaseModel):
	id: int
	item_id: int
	garage_id: Optional[int]
	operator_user_id: Optional[int]
	quantity: int
	minimum_quantity: int
	maximum_quantity: int
	item: ItemPublic
	class Config:
		from_attributes = True


class InventoryItemDetail(BaseModel):
	id: int
	quantity: int
	minimum_quantity: int
	maximum_quantity: int
	item: ItemPublic


class StockAddRequest(BaseModel):
	item_id: int
	garage_id: Optional[int] = None
	operator_user_id: Optional[int] = None
	quantity: int = Field(..., gt=0)


class UseItemRequest(BaseModel):
	item_id: int
	garage_id: Optional[int] = None
	operator_user_id: Optional[int] = None
	quantity: int = Field(..., gt=0)
	reference_ticket_id: Optional[int] = None

