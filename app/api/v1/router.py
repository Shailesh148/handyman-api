from fastapi import APIRouter, Depends
from app.core.security import require_auth

from .endpoints import users, locations, tickets, mechanic_profile, mechanic_assignment, admin, estimate

api_router = APIRouter(
    dependencies=[Depends(require_auth)]  # applies auth to ALL v1 endpoints
)

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(mechanic_profile.router, prefix="/mechanic_profile", tags=["mechanic_profile"])
api_router.include_router(mechanic_assignment.router, prefix="/mechanic_assignment", tags=["mechanic_assignment"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(estimate.router, prefix="/estimates", tags=["estimates"])
