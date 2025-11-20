
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.db import get_db
from app.models.service_type import ServiceType
from app.schemas.service_type import ServiceTypePublic


router = APIRouter()



@router.get("/", response_model=List[ServiceTypePublic])
def fetch_service_types(
    db: Session = Depends(get_db)
):
    return db.query(ServiceType).all()
    


