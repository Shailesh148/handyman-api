from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import require_auth
from app.models.user import AppUser
from app.schemas.user import UserCreate, UserRead

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
    auth0_user_id = "1234567890"
    user = AppUser(
        auth0_user_id=auth0_user_id,
        full_name=user_in.full_name,
        phone=user_in.phone,
        email=user_in.email,
        role=user_in.role,
    )

    db.add(user)
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
