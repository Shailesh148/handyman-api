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

from app.schemas.garage import GarageCreate, GaragePublic, GarageUserAssign
from app.schemas.item import ItemCreate, ItemPublic
from app.schemas.inventory import (
	InventoryCreate,
	InventoryPublic,
	StockAddRequest,
	UseItemRequest,
)


router = APIRouter()


def _validate_owner_ids(garage_id: Optional[int], operator_user_id: Optional[int]):
	if (garage_id is None and operator_user_id is None) or (garage_id is not None and operator_user_id is not None):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Provide exactly one of garage_id or operator_user_id",
		)


@router.post("/garages", response_model=GaragePublic, status_code=status.HTTP_201_CREATED)
def create_garage(garage_in: GarageCreate, db: Session = Depends(get_db)):
	garage = Garage(
		name=garage_in.name,
		phone=garage_in.phone,
		email=garage_in.email,
		address=garage_in.address,
		latitude=garage_in.latitude,
		longitude=garage_in.longitude,
	)
	db.add(garage)
	db.commit()
	db.refresh(garage)
	return garage


@router.post("/garages/{garage_id}/users", status_code=status.HTTP_201_CREATED)
def assign_user_to_garage(garage_id: int, assign_in: GarageUserAssign, db: Session = Depends(get_db)):
	garage = db.query(Garage).filter(Garage.id == garage_id).first()
	if not garage:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Garage not found")

	user = db.query(AppUser).filter(AppUser.id == assign_in.user_id).first()
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	existing = (
		db.query(GarageUser)
		.filter(and_(GarageUser.garage_id == garage_id, GarageUser.user_id == assign_in.user_id))
		.first()
	)
	if existing:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already assigned to this garage")

	link = GarageUser(garage_id=garage_id, user_id=assign_in.user_id, role=assign_in.role)
	db.add(link)
	db.commit()
	return {"message": "User assigned to garage"}


@router.post("/items", response_model=ItemPublic, status_code=status.HTTP_201_CREATED)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db)):
	item = Item(name=item_in.name, item_type=item_in.item_type, unit=item_in.unit)
	db.add(item)
	db.commit()
	db.refresh(item)
	return item


@router.post("/", response_model=InventoryPublic, status_code=status.HTTP_201_CREATED)
def create_inventory_record(inv_in: InventoryCreate, db: Session = Depends(get_db)):
	_validate_owner_ids(inv_in.garage_id, inv_in.operator_user_id)

	item = db.query(Item).filter(Item.id == inv_in.item_id).first()
	if not item:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

	existing = (
		db.query(Inventory)
		.filter(
			and_(
				Inventory.item_id == inv_in.item_id,
				Inventory.garage_id == inv_in.garage_id,
				Inventory.operator_user_id == inv_in.operator_user_id,
			)
		)
		.first()
	)
	if existing:
		# Update thresholds and optionally quantity if provided explicitly
		existing.minimum_quantity = inv_in.minimum_quantity
		existing.maximum_quantity = inv_in.maximum_quantity
		if inv_in.quantity is not None:
			existing.quantity = inv_in.quantity
		db.commit()
		db.refresh(existing)
		return existing

	inv = Inventory(
		item_id=inv_in.item_id,
		garage_id=inv_in.garage_id,
		operator_user_id=inv_in.operator_user_id,
		quantity=inv_in.quantity,
		minimum_quantity=inv_in.minimum_quantity,
		maximum_quantity=inv_in.maximum_quantity,
	)
	db.add(inv)
	db.commit()
	db.refresh(inv)
	return inv


@router.post("/add_item", response_model=InventoryPublic)
def add_items_to_inventory(payload: StockAddRequest, db: Session = Depends(get_db)):
	_validate_owner_ids(payload.garage_id, payload.operator_user_id)

	inv = (
		db.query(Inventory)
		.filter(
			and_(
				Inventory.item_id == payload.item_id,
				Inventory.garage_id == payload.garage_id,
				Inventory.operator_user_id == payload.operator_user_id,
			)
		)
		.first()
	)
	if not inv:
		# create record if missing
		inv = Inventory(
			item_id=payload.item_id,
			garage_id=payload.garage_id,
			operator_user_id=payload.operator_user_id,
			quantity=0,
		)
		db.add(inv)
		db.flush()

	inv.quantity = (inv.quantity or 0) + payload.quantity
	db.add(
		InventoryTransaction(
			item_id=payload.item_id,
			garage_id=payload.garage_id,
			operator_user_id=payload.operator_user_id,
			quantity_change=payload.quantity,
			transaction_type=InventoryTransactionType.PURCHASED,
		)
	)
	db.commit()
	db.refresh(inv)
	return inv


@router.post("/use_item", response_model=InventoryPublic)
def use_item_from_inventory(payload: UseItemRequest, db: Session = Depends(get_db)):
	_validate_owner_ids(payload.garage_id, payload.operator_user_id)

	inv = (
		db.query(Inventory)
		.filter(
			and_(
				Inventory.item_id == payload.item_id,
				Inventory.garage_id == payload.garage_id,
				Inventory.operator_user_id == payload.operator_user_id,
			)
		)
		.first()
	)
	if not inv:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory record not found")

	if (inv.quantity or 0) < payload.quantity:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient quantity")

	inv.quantity = (inv.quantity or 0) - payload.quantity
	db.add(
		InventoryTransaction(
			item_id=payload.item_id,
			garage_id=payload.garage_id,
			operator_user_id=payload.operator_user_id,
			quantity_change= -payload.quantity,
			transaction_type=InventoryTransactionType.USED_ON_JOB,
			reference_ticket_id=payload.reference_ticket_id,
		)
	)
	db.commit()
	db.refresh(inv)
	return inv

