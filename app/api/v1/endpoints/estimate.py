
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.estimate import EstimateUpdate, EstimateCreate
from app.services.estimate_service import (
    modify_estimate as svc_modify_estimate,
    create_estimate as svc_create_estimate,
)
router = APIRouter()


@router.put("/", response_model = str, status_code=status.HTTP_201_CREATED)
def modify_estimate(
    estimate_in: EstimateUpdate, 
    db: Session = Depends(get_db)
):
    return svc_modify_estimate(db, estimate_in)


@router.post("/", response_model = str, status_code=status.HTTP_201_CREATED)
def create_estimate(
    estimate_in: EstimateCreate, 
    db: Session = Depends(get_db)
):
    return svc_create_estimate(db, estimate_in)