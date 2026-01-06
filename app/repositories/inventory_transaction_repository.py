from sqlalchemy.orm import Session
from app.models.inventory_transaction import InventoryTransaction


def create_transaction(
    db: Session,
    *,
    item_id: int,
    garage_id: int | None,
    operator_user_id: int | None,
    quantity_change: int,
    transaction_type: str,
    reference_ticket_id: int | None = None,
) -> InventoryTransaction:
    tx = InventoryTransaction(
        item_id=item_id,
        garage_id=garage_id,
        operator_user_id=operator_user_id,
        quantity_change=quantity_change,
        transaction_type=transaction_type,
        reference_ticket_id=reference_ticket_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


