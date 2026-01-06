from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.db import get_db
from app.schemas.service_type import ServiceTypePublic
from app.services.service_type_service import list_service_types as svc_list_service_types
router = APIRouter()



@router.get("/", response_model=List[ServiceTypePublic])
def fetch_service_types(
    db: Session = Depends(get_db)
):
    return svc_list_service_types(db)
    

