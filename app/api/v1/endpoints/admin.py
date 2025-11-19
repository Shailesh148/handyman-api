from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.estimate import EstimatePublic, EstimateUpdate
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.estimate import Estimate
from app.models.mechanic_assignment import MechanicAssignmentModel
from app.models.ticket import Ticket
from app.models.location import Location
from app.models.mechanic_profile import MechanicProfile
from app.models.user import AppUser

router = APIRouter()



@router.delete("/user")
def reset_user_data(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        user = db.query(AppUser).filter(AppUser.id == user_id).first()

        # 4. Delete tickets created by user (as customer)
        # This will cascade delete ticket_status_history, estimates, assignments linked to the ticket
        db.query(Ticket).filter(Ticket.customer_id == user_id).delete(synchronize_session=False)

        # 7. Delete mechanic profile
        db.query(MechanicProfile).filter(MechanicProfile.user_id == user_id).delete(synchronize_session=False)

        # # 5. Delete vehicles
        # db.query(Vehicle).filter(Vehicle.user_id == user_id).delete(synchronize_session=False)

        # 6. Delete locations
        db.query(Location).filter(Location.user_id == user_id).delete(synchronize_session=False)

        # 8. Finally, delete the user
        db.delete(user)

        # Commit all deletions
        db.commit()

        return {"message": f"User with id {user_id} and all associated data deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error deleting user data: {str(e)}"
        )
    
