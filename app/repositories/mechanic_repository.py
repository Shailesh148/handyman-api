from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.mechanic_profile import MechanicProfile
from app.models.mechanic_service_type import MechanicServiceType


def create_mechanic_profile(db: Session, user_id: int) -> MechanicProfile:
    profile = MechanicProfile(user_id=user_id)
    db.add(profile)
    db.flush()
    db.refresh(profile)
    return profile


def get_mechanic_profile_by_user_id(db: Session, user_id: int) -> Optional[MechanicProfile]:
    return db.query(MechanicProfile).filter(MechanicProfile.user_id == user_id).first()


def create_mechanic_service_link(db: Session, mechanic_id: int, service_type_id: int) -> MechanicServiceType:
    link = MechanicServiceType(mechanic_id=mechanic_id, service_type_id=service_type_id)
    db.add(link)
    db.flush()
    db.refresh(link)
    return link


def list_service_links_for_mechanic(db: Session, mechanic_id: int) -> List[MechanicServiceType]:
    return db.query(MechanicServiceType).filter(MechanicServiceType.mechanic_id == mechanic_id).all()


def delete_mechanic_profile_by_user_id(db: Session, user_id: int) -> None:
    db.query(MechanicProfile).filter(MechanicProfile.user_id == user_id).delete(synchronize_session=False)


