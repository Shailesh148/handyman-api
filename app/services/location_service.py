from typing import List
from sqlalchemy.orm import Session
from app.schemas.location import LocationCreate, LocationPublic
from app.repositories.location_repository import (
    create_location as repo_create_location,
    list_locations_by_user_id as repo_list_locations_by_user_id,
)


def create_location(db: Session, location_in: LocationCreate):
    return repo_create_location(db, location_in)


def list_user_locations(db: Session, user_id: int):
    return repo_list_locations_by_user_id(db, user_id)


