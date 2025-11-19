
from fastapi import APIRouter, status, Depends
from app.schemas.estimate import EstimatePublic, EstimateUpdate
from sqlalchemy.orm import Session
from app.core.db import get_db


router = APIRouter()


# @router.post("/", response_model = EstimatePublic, status_code=status.HTTP_201_CREATED)
# def modify_estimate(
#     estimate_in: EstimateUpdate, 
#     db: Session = Depends(get_db)
# ):
    