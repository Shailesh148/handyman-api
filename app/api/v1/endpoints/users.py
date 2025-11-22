from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import require_auth
from app.models.user import AppUser
from app.schemas.user import UserCreate, UserRead, UserPublic
from app.schemas.mechanic_profile import MechanicCreate
from app.models.mechanic_profile import MechanicProfile
from app.models.mechanic_service_type import MechanicServiceType
import random
import string
router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    token_payload: Dict[str, Any] = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Create an app_user row for the currently authenticated Auth0 user.

    - Uses `sub` from Auth0 token as `auth0_user_id`
    - Enforces unique auth0_user_id & phone
    """
    # auth0_user_id = token_payload.get("sub")
    # if not auth0_user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Invalid token: missing 'sub'",
    #     )

    # # Optional: if user already exists, you can either return it or error.
    # existing = (
    #     db.query(AppUser)
    #     .filter(AppUser.auth0_user_id == auth0_user_id)
    #     .first()
    # )
    # if existing:
    #     # You can change this to update & return if that's preferred.
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="User already registered",
    #     )
    auth0_user_id = ''.join(random.choices(string.digits, k=10))
    user = AppUser(
        auth0_user_id=auth0_user_id,
        full_name=user_in.full_name,
        phone=user_in.phone,
        email=user_in.email,
        role=user_in.role,
    )

    db.add(user)
    db.flush()
    if user_in.role == "MECHANIC":
        new_mechanic = MechanicProfile(
            user_id=user.id,
            # base_location_id = mechanic.mechanic_location_id,
        )

        db.add(new_mechanic)
        db.flush()
        
        for each_service_id in user_in.service_type_ids:
            new_mechanic_service = MechanicServiceType(
                mechanic_id = new_mechanic.id,
                service_type_id = each_service_id
            )

            db.add(new_mechanic_service)
        
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone or Auth0 user already exists",
        )

    db.refresh(user)
    return user



# 🔹 NEW: fetch user by email, safe public data only
@router.get("/by-email", response_model=UserPublic)
def get_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    token_payload: Dict[str, Any] = Depends(require_auth),
):
    """
    Fetch a user by email.

    - Requires Auth0 token in Authorization header
    - Returns public user data only (no DB id, no auth0_user_id)
    """
    user = db.query(AppUser).filter(AppUser.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.get("/by-phone", response_model=UserPublic)
def get_user_by_phone(
    phone: str,
    db: Session = Depends(get_db),
    token_payload: Dict[str, Any] = Depends(require_auth),
):
    """
    Fetch a user by email.

    - Requires Auth0 token in Authorization header
    - Returns public user data only (no DB id, no auth0_user_id)
    """
    print(phone)
    user = db.query(AppUser).filter(AppUser.phone == phone).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user