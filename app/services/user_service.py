from typing import List, Optional
import random
import string
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import AppUser, UserRole
from app.models.mechanic_profile import MechanicProfile
from app.schemas.user import UserCreate, UserPublic
from app.schemas.service_type import ServiceTypePublic

from app.repositories.user_repository import (
    create_user as repo_create_user,
    get_user_by_email as repo_get_user_by_email,
    get_user_by_phone as repo_get_user_by_phone,
    get_users_by_role as repo_get_users_by_role,
)
from app.repositories.mechanic_repository import (
    create_mechanic_profile,
    list_service_links_for_mechanic,
)
from app.repositories.service_type_repository import get_service_type_by_id


def generate_auth0_user_id() -> str:
    return "".join(random.choices(string.digits, k=10))


def create_user(db: Session, user_in: UserCreate) -> AppUser:
    auth0_user_id = generate_auth0_user_id()
    user = AppUser(
        auth0_user_id=auth0_user_id,
        full_name=user_in.full_name,
        phone=user_in.phone,
        email=user_in.email,
        role=user_in.role,
    )

    try:
        repo_create_user(db, user)
        if user_in.role == UserRole.MECHANIC:
            mechanic_profile: MechanicProfile = create_mechanic_profile(db, user.id)
            for service_type_id in user_in.service_type_ids:
                # Create links
                from app.repositories.mechanic_repository import create_mechanic_service_link

                create_mechanic_service_link(
                    db, mechanic_id=mechanic_profile.id, service_type_id=service_type_id
                )
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone or Auth0 user already exists",
        )


def get_user_by_email(db: Session, email: str) -> Optional[AppUser]:
    return repo_get_user_by_email(db, email)


def get_user_by_phone(db: Session, phone: str) -> Optional[AppUser]:
    return repo_get_user_by_phone(db, phone)


def list_mechanics_with_services(db: Session) -> List[UserPublic]:
    mechanics = repo_get_users_by_role(db, UserRole.MECHANIC)
    result: List[UserPublic] = []
    for mechanic_user in mechanics:
        mechanic_profile = create_or_get_mechanic_profile(db, mechanic_user.id)
        service_links = list_service_links_for_mechanic(db, mechanic_profile.id)
        service_types_public: List[ServiceTypePublic] = []
        for link in service_links:
            st = get_service_type_by_id(db, link.service_type_id)
            if st:
                service_types_public.append(
                    ServiceTypePublic(
                        id=st.id,
                        category_id=st.category_id,
                        name=st.name,
                        description=st.description,
                    )
                )
        result.append(
            UserPublic(
                id=mechanic_user.id,
                full_name=mechanic_user.full_name,
                phone=mechanic_user.phone,
                email=mechanic_user.email,
                role=mechanic_user.role,
                is_active=mechanic_user.is_active,
                mechanic_services=service_types_public,
            )
        )
    return result


def list_operators(db: Session) -> List[AppUser]:
    return repo_get_users_by_role(db, UserRole.OPERATOR)


def create_or_get_mechanic_profile(db: Session, user_id: int) -> MechanicProfile:
    from app.repositories.mechanic_repository import get_mechanic_profile_by_user_id

    profile = get_mechanic_profile_by_user_id(db, user_id)
    if profile is None:
        profile = create_mechanic_profile(db, user_id)
        db.commit()
        db.refresh(profile)
    return profile


