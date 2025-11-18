from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.utils.user_utils import get_current_user
from app.core.db import get_db
from app.models.location import Location
from app.models.ticket import Ticket, TicketStatus
from app.models.user import AppUser
from app.schemas.ticket import TicketCreate, TicketPublic
from app.models.service_type import ServiceType
from app.models.service_issue import ServiceIssue

router = APIRouter()


def generate_ticket_code() -> str:
    # Simple time-based code, good enough to start with
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"JOB-{ts}"


@router.post(
    "/", response_model=TicketPublic, status_code=status.HTTP_201_CREATED,
    summary="Create a new ticket (job) for current user"
)
def create_ticket(
    email: str,
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
):
    # 1) Verify location belongs to current user
    # location = (
    #     db.query(Location)
    #     .filter(
    #         Location.id == ticket_in.customer_location_id,
    #         Location.user_id == current_user.id,
    #     )
    #     .first()
    # )
    # if not location:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Invalid location: does not belong to current user",
    #     )

    # TODO (optional): verify service_issue_id exists; verify vehicle_id belongs to user
    service_type = (
        db.query(ServiceType)
        .filter(
            ServiceType.name == ticket_in.category
        )
        .first()
    )
    
    service_issue = ServiceIssue(
        service_type_id = service_type.id,
        name = ticket_in.category,
        description = ticket_in.description
    )

    db.add(service_issue)
    db.flush()

    ticket = Ticket(
        ticket_code=generate_ticket_code(),
        customer_id=current_user.id,
        service_issue_id=service_issue.id,
        customer_location_id=ticket_in.customer_location_id,
        status=TicketStatus.REQUESTED,
        description=ticket_in.description,
    )
    
    # if "vehicle_id" in ticket_in:
    #     ticket["vehicle_id"] = ticket_in.vehicle_id
    print(ticket)
    db.add(ticket)

    db.commit() 
    db.refresh(ticket) 
    return ticket
