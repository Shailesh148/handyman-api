from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.inventory import Inventory


def get_inventory_record(
    db: Session, item_id: int, garage_id: Optional[int], operator_user_id: Optional[int]
) -> Optional[Inventory]:
    return (
        db.query(Inventory)
        .filter(
            and_(
                Inventory.item_id == item_id,
                Inventory.garage_id == garage_id,
                Inventory.operator_user_id == operator_user_id,
            )
        )
        .first()
    )


def create_inventory(
    db: Session,
    item_id: int,
    garage_id: Optional[int],
    operator_user_id: Optional[int],
    quantity: Optional[int],
    minimum_quantity: Optional[int],
    maximum_quantity: Optional[int],
) -> Inventory:
    inv = Inventory(
        item_id=item_id,
        garage_id=garage_id,
        operator_user_id=operator_user_id,
        quantity=quantity,
        minimum_quantity=minimum_quantity,
        maximum_quantity=maximum_quantity,
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv


def save_inventory(db: Session, inv: Inventory) -> Inventory:
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv


