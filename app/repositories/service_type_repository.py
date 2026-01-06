from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.service_type import ServiceType


def list_service_types(db: Session) -> List[ServiceType]:
    return db.query(ServiceType).all()


def get_service_type_by_id(db: Session, service_type_id: int) -> Optional[ServiceType]:
    return db.query(ServiceType).filter(ServiceType.id == service_type_id).first()


def get_service_type_by_name(db: Session, name: str) -> Optional[ServiceType]:
    return db.query(ServiceType).filter(ServiceType.name == name).first()


