from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.schemas.user_device import UserDeviceCreate
from app.core.db import get_db
from app.services.user_device_service import create_user_device as svc_create_user_device
router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user_device(user_device_in: UserDeviceCreate, db: Session = Depends(get_db)):
    svc_create_user_device(db, user_device_in)
    