from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.db import get_db
from app.models.user import AppUser
from app.models.garage import Garage, GarageUser
from app.models.item import Item
from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction, InventoryTransactionType

from app.schemas.garage import GarageCreate, GaragePublic, GarageUserAssign, AllGaragesPublic
from app.schemas.item import ItemCreate, ItemPublic
from app.schemas.inventory import (
	InventoryCreate,
	InventoryPublic,
	StockAddRequest,
	UseItemRequest,
	InventoryItemDetail,
)
import threading
from app.common.messaging import send_admin_reorder_notification
from app.services.inventory_service import (
	list_garages as svc_list_garages,
	create_garage as svc_create_garage,
	assign_user_to_garage as svc_assign_user_to_garage,
	create_item as svc_create_item,
	list_items as svc_list_items,
	create_inventory as svc_create_inventory,
	get_garage as svc_get_garage,
	add_items_to_inventory as svc_add_items_to_inventory,
	use_item_from_inventory as svc_use_item_from_inventory,
)


router = APIRouter()


def _validate_owner_ids(garage_id: Optional[int], operator_user_id: Optional[int]):
	if (garage_id is None and operator_user_id is None) or (garage_id is not None and operator_user_id is not None):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Provide exactly one of garage_id or operator_user_id",
		)


@router.get("/garages", response_model=List[AllGaragesPublic])
def get_all_garages(db: Session = Depends(get_db)):
	return svc_list_garages(db)


@router.post("/garages", response_model=GaragePublic, status_code=status.HTTP_201_CREATED)
def create_garage(garage_in: GarageCreate, db: Session = Depends(get_db)):
	return svc_create_garage(db, garage_in)


@router.post("/garages/{garage_id}/users", status_code=status.HTTP_201_CREATED)
def assign_user_to_garage(garage_id: int, assign_in: GarageUserAssign, db: Session = Depends(get_db)):
	return svc_assign_user_to_garage(db, garage_id, assign_in)


@router.post("/items", response_model=ItemPublic, status_code=status.HTTP_201_CREATED)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db)):
	return svc_create_item(db, item_in)

@router.get("/items", response_model=List[ItemPublic])
def get_all_items(db: Session = Depends(get_db)):
	return svc_list_items(db)


@router.post("/", response_model=InventoryPublic, status_code=status.HTTP_201_CREATED)
def create_inventory_record(inv_in: InventoryCreate, db: Session = Depends(get_db)):
	return svc_create_inventory(db, inv_in)


@router.get("/garages/{garage_id}", response_model=GaragePublic)
def fetch_garage_inventory(garage_id: int, db: Session = Depends(get_db)):
	garage = svc_get_garage(db, garage_id)
	# if not garage:
	# 	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Garage not found")

	# rows = (
	# 	db.query(Inventory, Item, Garage)
	# 	.join(Item, Inventory.item_id == Item.id)
	# 	.join(Garage, Inventory.garage_id == Garage.id)
	# 	.filter(Inventory.garage_id == garage_id)
	# 	.all()
	# )

	# result: List[InventoryItemDetail] = []
	# for inv, item, gar in rows:
	# 	result.append(
	# 		InventoryItemDetail(
	# 			id=inv.id,
	# 			quantity=inv.quantity or 0,
	# 			minimum_quantity=inv.minimum_quantity or 0,
	# 			maximum_quantity=inv.maximum_quantity or 0,
	# 			item=ItemPublic(
	# 				id=item.id,
	# 				name=item.name,
	# 				item_type=item.item_type,  # enum is fine with Pydantic
	# 				unit=item.unit,
	# 			),
	# 		)
	# 	)
	return garage


@router.post("/add_item", response_model=InventoryPublic)
def add_items_to_inventory(payload: StockAddRequest, db: Session = Depends(get_db)):
	return svc_add_items_to_inventory(db, payload)


@router.post("/use_item", response_model=InventoryPublic)
def use_item_from_inventory(payload: UseItemRequest, db: Session = Depends(get_db)):
	return svc_use_item_from_inventory(db, payload)

