from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.item import Item


def create_item(db: Session, item: Item) -> Item:
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_items(db: Session) -> List[Item]:
    return db.query(Item).all()


def get_item_by_id(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()


