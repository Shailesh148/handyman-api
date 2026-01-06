from typing import List
from sqlalchemy.orm import Session
from app.models.location import Location
from app.schemas.location import LocationCreate


def create_location(db: Session, location_in: LocationCreate) -> Location:
    loc = Location(
        user_id=location_in.user_id,
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


def list_locations_by_user_id(db: Session, user_id: int) -> List[Location]:
    return (
        db.query(Location)
        .filter(Location.user_id == user_id)
        .order_by(Location.created_at.desc())
        .all()
    )


def delete_locations_by_user_id(db: Session, user_id: int) -> None:
    db.query(Location).filter(Location.user_id == user_id).delete(synchronize_session=False)


