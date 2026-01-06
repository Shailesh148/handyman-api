from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.location import LocationCreate, LocationPublic
from app.services.location_service import (
    create_location as svc_create_location,
    list_user_locations as svc_list_user_locations,
)
router = APIRouter()


@router.post(
    "/", response_model=LocationPublic, summary="Add a location for current user"
)
def create_location(
    # email: str,
    location_in: LocationCreate,
    db: Session = Depends(get_db),
    # current_user: AppUser = Depends(get_current_user),
):
    # If new location is primary, unset existing primary for this user
    # if location_in.is_primary:
    #     (
    #         db.query(Location)
    #         .filter(Location.user_id == current_user.id, Location.is_primary == True)
    #         .update({"is_primary": False})
    #     )

    return svc_create_location(db, location_in)


@router.get(
    "/", response_model=List[LocationPublic], summary="List current user's locations"
)
def list_my_locations(
    # email: str,
    user_id: str,
    db: Session = Depends(get_db),
    # current_user: AppUser = Depends(get_current_user),
):
    return svc_list_user_locations(db, int(user_id))
