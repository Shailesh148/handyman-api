from sqlalchemy.orm import Session
from app.models.user_device import UserDevice
from app.schemas.user_device import UserDeviceCreate


def create_user_device(db: Session, payload: UserDeviceCreate) -> UserDevice:
    user_device = UserDevice(user_id=payload.user_id, fcm_token=payload.fcm_token)
    db.add(user_device)
    db.commit()
    db.refresh(user_device)
    return user_device


