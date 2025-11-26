
from fastapi import APIRouter, status, Depends
from app.models.user_device import UserDevice
from app.schemas.user_device import UserDeviceCreate
from sqlalchemy.orm import Session
from typing import Optional

from app.core.db import get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user_device(user_device_in: UserDeviceCreate, db: Session = Depends(get_db)):
    try:
        user_device = UserDevice(
            user_id = user_device_in.user_id,
            fcm_token = user_device_in.fcm_token
        )

        db.add(user_device)
        
        db.commit()
    except Exception as e:
        db.rollback()
        print("Error in creating user device")
    