# app/routers/mechanics.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.core.db import get_db
from app.models.mechanic_profile import MechanicProfile  # SQLAlchemy model
from app.schemas.mechanic_profile import MechanicCreate, MechanicResponse
from app.models.user import AppUser
from app.models.mechanic_service_type import MechanicServiceType

router = APIRouter()

@router.post("/", response_model=MechanicResponse, status_code=status.HTTP_201_CREATED)
def create_mechanic(mechanic: MechanicCreate, db: Session = Depends(get_db)):
    """
    Create a new mechanic profile.
    """
    # Check if mechanic with same email exists
    # existing_mechanic = db.query(MechanicProfile).filter(MechanicProfile.email == mechanic.email).first()
    # if existing_mechanic:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Mechanic with this email already exists."
    #     )
    existing_user_id = (
        db.query(AppUser)
        .filter(
            AppUser.email == mechanic.email
        )
        .first()
    )
    # Create new mechanic
    new_mechanic = MechanicProfile(
        user_id=existing_user_id.id,
        base_location_id = mechanic.mechanic_location_id,
    )

    db.add(new_mechanic)
    db.flush()
    
    for each_service_id in mechanic.service_type_ids:
        new_mechanic_service = MechanicServiceType(
            mechanic_id = new_mechanic.id,
            service_type_id = each_service_id
        )

        db.add(new_mechanic_service)
        db.flush()
    
    db.commit() 
    db.refresh(new_mechanic)

    return new_mechanic
