from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.user_utils import get_current_user
from app.core.db import get_db
from app.models.location import Location
from app.models.user import AppUser
from app.schemas.location import LocationCreate, LocationPublic

router = APIRouter()


@router.post(
    "/", response_model=LocationPublic, summary="Add a location for current user"
)
def create_location(
    email: str,
    location_in: LocationCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
):
    # If new location is primary, unset existing primary for this user
    if location_in.is_primary:
        (
            db.query(Location)
            .filter(Location.user_id == current_user.id, Location.is_primary == True)
            .update({"is_primary": False})
        )

    loc = Location(
        user_id=current_user.id,
        label=location_in.label,
        address_line1=location_in.address_line1,
        address_line2=location_in.address_line2,
        city=location_in.city,
        state=location_in.state,
        postal_code=location_in.postal_code,
        latitude=location_in.latitude,
        longitude=location_in.longitude,
        is_primary=location_in.is_primary,
    )

    db.add(loc)
    db.commit()
    db.refresh(loc)
    return loc


@router.get(
    "/", response_model=List[LocationPublic], summary="List current user's locations"
)
def list_my_locations(
    email: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
):
    locations = (
        db.query(Location)
        .filter(Location.user_id == current_user.id)
        .order_by(Location.created_at.desc())
        .all()
    )
    return locations
