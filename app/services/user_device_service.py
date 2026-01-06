from sqlalchemy.orm import Session
from app.schemas.user_device import UserDeviceCreate
from app.repositories.user_device_repository import create_user_device as repo_create_user_device


def create_user_device(db: Session, payload: UserDeviceCreate) -> None:
    try:
        repo_create_user_device(db, payload)
    except Exception:
        db.rollback()
        # Swallowing exception to match prior behavior of just printing error
        # Could be enhanced to raise HTTPException or log
        pass


