from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.admin_service import reset_user_data as svc_reset_user_data
router = APIRouter()



@router.delete("/user")
def reset_user_data(
    user_id: int,
    db: Session = Depends(get_db)
):
    return svc_reset_user_data(db, user_id)
    
