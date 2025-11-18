from fastapi import APIRouter, Depends
from app.core.security import require_auth

from .endpoints import users

api_router = APIRouter(
    dependencies=[Depends(require_auth)]  # applies auth to ALL v1 endpoints
)

api_router.include_router(users.router, prefix="/users", tags=["users"])
