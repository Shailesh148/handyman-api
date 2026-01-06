from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import require_auth
from app.schemas.user import UserCreate, UserRead, UserPublic
from app.services.user_service import (
    create_user as svc_create_user,
    get_user_by_email as svc_get_user_by_email,
    get_user_by_phone as svc_get_user_by_phone,
    list_mechanics_with_services as svc_list_mechanics_with_services,
    list_operators as svc_list_operators,
)
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
    return svc_create_user(db, user_in)



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
    user = svc_get_user_by_email(db, email)

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
    user = svc_get_user_by_phone(db, phone)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user

@router.get("/mechanic/all", response_model=List[UserPublic])
def get_all_mechanics(
    db: Session = Depends(get_db),
    token_payload: Dict[str, Any] = Depends(require_auth),
):
    """
    Fetch a user by email.

    - Requires Auth0 token in Authorization header
    - Returns public user data only (no DB id, no auth0_user_id)
    """
    return svc_list_mechanics_with_services(db)




@router.get("/operator/all", response_model=List[UserPublic])
def get_all_operators(
    db: Session = Depends(get_db),
    token_payload: Dict[str, Any] = Depends(require_auth),
):
    """
    Fetch a user by email.

    - Requires Auth0 token in Authorization header
    - Returns public user data only (no DB id, no auth0_user_id)
    """
    return svc_list_operators(db)
    
    