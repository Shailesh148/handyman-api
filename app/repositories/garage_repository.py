from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.garage import Garage, GarageUser


def list_garages(db: Session) -> List[Garage]:
    return db.query(Garage).all()


def create_garage(db: Session, garage: Garage) -> Garage:
    db.add(garage)
    db.commit()
    db.refresh(garage)
    return garage


def get_garage_by_id(db: Session, garage_id: int) -> Optional[Garage]:
    return db.query(Garage).filter(Garage.id == garage_id).first()


def get_garage_user_link(db: Session, garage_id: int, user_id: int) -> Optional[GarageUser]:
    return (
        db.query(GarageUser)
        .filter(and_(GarageUser.garage_id == garage_id, GarageUser.user_id == user_id))
        .first()
    )


def create_garage_user_link(db: Session, garage_id: int, user_id: int, role: Optional[str]) -> GarageUser:
    link = GarageUser(garage_id=garage_id, user_id=user_id, role=role)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


