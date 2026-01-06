from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import AppUser, UserRole


def create_user(db: Session, user: AppUser) -> AppUser:
    db.add(user)
    db.flush()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[AppUser]:
    return db.query(AppUser).filter(AppUser.email == email).first()


def get_user_by_phone(db: Session, phone: str) -> Optional[AppUser]:
    return db.query(AppUser).filter(AppUser.phone == phone).first()


def get_users_by_role(db: Session, role: UserRole) -> List[AppUser]:
    return db.query(AppUser).filter(AppUser.role == role).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[AppUser]:
    return db.query(AppUser).filter(AppUser.id == user_id).first()


def delete_user(db: Session, user: AppUser) -> None:
    db.delete(user)


