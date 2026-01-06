from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import get_user_by_id, delete_user
from app.repositories.ticket_repository import delete_tickets_by_customer_id
from app.repositories.mechanic_repository import delete_mechanic_profile_by_user_id
from app.repositories.location_repository import delete_locations_by_user_id


def reset_user_data(db: Session, user_id: int):
    try:
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        delete_tickets_by_customer_id(db, user_id)
        delete_mechanic_profile_by_user_id(db, user_id)
        delete_locations_by_user_id(db, user_id)
        delete_user(db, user)
        db.commit()
        return {"message": f"User with id {user_id} and all associated data deleted successfully"}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user data: {str(e)}",
        )


