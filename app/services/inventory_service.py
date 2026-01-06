from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.garage import Garage, GarageUser
from app.models.item import Item
from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransactionType
from app.schemas.garage import GarageCreate, GaragePublic, GarageUserAssign, AllGaragesPublic
from app.schemas.item import ItemCreate, ItemPublic
from app.schemas.inventory import (
    InventoryCreate,
    InventoryPublic,
    StockAddRequest,
    UseItemRequest,
    InventoryItemDetail,
)
from app.repositories.garage_repository import (
    list_garages as repo_list_garages,
    create_garage as repo_create_garage,
    get_garage_by_id as repo_get_garage_by_id,
    get_garage_user_link as repo_get_garage_user_link,
    create_garage_user_link as repo_create_garage_user_link,
)
from app.repositories.item_repository import (
    create_item as repo_create_item,
    list_items as repo_list_items,
    get_item_by_id as repo_get_item_by_id,
)
from app.repositories.inventory_repository import (
    get_inventory_record as repo_get_inventory_record,
    create_inventory as repo_create_inventory,
    save_inventory as repo_save_inventory,
)
from app.repositories.inventory_transaction_repository import create_transaction as repo_create_transaction
from app.repositories.user_repository import get_user_by_id as repo_get_user_by_id
from app.common.messaging import send_admin_reorder_notification
import threading


def _validate_owner_ids(garage_id: Optional[int], operator_user_id: Optional[int]):
    if (garage_id is None and operator_user_id is None) or (
        garage_id is not None and operator_user_id is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide exactly one of garage_id or operator_user_id",
        )


def list_garages(db: Session) -> List[AllGaragesPublic]:
    return repo_list_garages(db)


def create_garage(db: Session, garage_in: GarageCreate) -> GaragePublic:
    garage = Garage(
        name=garage_in.name,
        phone=garage_in.phone,
        email=garage_in.email,
        address=garage_in.address,
        latitude=garage_in.latitude,
        longitude=garage_in.longitude,
        type=garage_in.type,
    )
    return repo_create_garage(db, garage)


def assign_user_to_garage(db: Session, garage_id: int, assign_in: GarageUserAssign):
    garage = repo_get_garage_by_id(db, garage_id)
    if not garage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Garage not found")
    user = repo_get_user_by_id(db, assign_in.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    existing = repo_get_garage_user_link(db, garage_id, assign_in.user_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already assigned to this garage"
        )
    repo_create_garage_user_link(db, garage_id, assign_in.user_id, assign_in.role)
    return {"message": "User assigned to garage"}


def create_item(db: Session, item_in: ItemCreate) -> ItemPublic:
    item = Item(name=item_in.name, item_type=item_in.item_type, unit=item_in.unit)
    return repo_create_item(db, item)


def list_items(db: Session) -> List[ItemPublic]:
    return repo_list_items(db)


def create_inventory(db: Session, inv_in: InventoryCreate) -> InventoryPublic:
    _validate_owner_ids(inv_in.garage_id, inv_in.operator_user_id)
    item = repo_get_item_by_id(db, inv_in.item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    existing = repo_get_inventory_record(db, inv_in.item_id, inv_in.garage_id, inv_in.operator_user_id)
    if existing:
        existing.minimum_quantity = inv_in.minimum_quantity
        existing.maximum_quantity = inv_in.maximum_quantity
        if inv_in.quantity is not None:
            existing.quantity = inv_in.quantity
        return repo_save_inventory(db, existing)
    return repo_create_inventory(
        db,
        item_id=inv_in.item_id,
        garage_id=inv_in.garage_id,
        operator_user_id=inv_in.operator_user_id,
        quantity=inv_in.quantity,
        minimum_quantity=inv_in.minimum_quantity,
        maximum_quantity=inv_in.maximum_quantity,
    )


def get_garage(db: Session, garage_id: int) -> GaragePublic:
    return repo_get_garage_by_id(db, garage_id)


def add_items_to_inventory(db: Session, payload: StockAddRequest) -> InventoryPublic:
    _validate_owner_ids(payload.garage_id, payload.operator_user_id)
    inv = repo_get_inventory_record(
        db, payload.item_id, payload.garage_id, payload.operator_user_id
    )
    if not inv:
        inv = Inventory(
            item_id=payload.item_id,
            garage_id=payload.garage_id,
            operator_user_id=payload.operator_user_id,
            quantity=0,
        )
        repo_save_inventory(db, inv)
    inv.quantity = (inv.quantity or 0) + payload.quantity
    repo_save_inventory(db, inv)
    repo_create_transaction(
        db,
        item_id=payload.item_id,
        garage_id=payload.garage_id,
        operator_user_id=payload.operator_user_id,
        quantity_change=payload.quantity,
        transaction_type=InventoryTransactionType.PURCHASED,
    )
    return inv


def use_item_from_inventory(db: Session, payload: UseItemRequest) -> InventoryPublic:
    _validate_owner_ids(payload.garage_id, payload.operator_user_id)
    inv = repo_get_inventory_record(
        db, payload.item_id, payload.garage_id, payload.operator_user_id
    )
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory record not found")
    if (inv.quantity or 0) < payload.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient quantity")
    inv.quantity = (inv.quantity or 0) - payload.quantity
    repo_save_inventory(db, inv)
    repo_create_transaction(
        db,
        item_id=payload.item_id,
        garage_id=payload.garage_id,
        operator_user_id=payload.operator_user_id,
        quantity_change=-payload.quantity,
        transaction_type=InventoryTransactionType.USED_ON_JOB,
        reference_ticket_id=payload.reference_ticket_id,
    )
    if inv.quantity <= inv.minimum_quantity:
        thread = threading.Thread(
            send_admin_reorder_notification("ADMIN", "reorder_inventory", inv)
        )
        thread.start()
    return inv


