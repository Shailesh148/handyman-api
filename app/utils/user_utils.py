# app/api/deps.py
from typing import Dict, Any

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import require_auth
from app.models.user import AppUser


def get_current_user(
    email: str,
    token_payload: Dict[str, Any] = Depends(require_auth),
    db: Session = Depends(get_db)
) -> AppUser:
    # auth0_user_id = token_payload.get("sub")
    # if not auth0_user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Invalid token: missing 'sub'",
    #     )

    user = (
        db.query(AppUser)
        .filter(AppUser.email == email)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found for this Auth0 account",
        )

    return user
