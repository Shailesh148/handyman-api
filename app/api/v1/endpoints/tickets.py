from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.utils.user_utils import get_current_user
from app.core.db import get_db
from app.models.location import Location
from app.models.ticket import Ticket, TicketStatus
from app.models.user import AppUser
from app.schemas.ticket import TicketCreate, TicketPublic
from app.models.service_type import ServiceType
from app.models.service_issue import ServiceIssue
from sqlalchemy.orm import Session, joinedload

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
    # email: str,
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
    # current_user: AppUser = Depends(get_current_user),
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
            ServiceType.name == ticket_in.service
        )
        .first()
    )
    
    service_issue = ServiceIssue(
        service_type_id = service_type.id,
        name = ticket_in.service,
        description = ticket_in.description
    )

    db.add(service_issue)
    db.flush()

    ticket = Ticket(
        ticket_code=generate_ticket_code(),
        customer_id=ticket_in.user_id,
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




# fetch user's ticket
@router.get("/", response_model=List[TicketPublic])
def fetch_user_ticket(
    user_id: int, 
    db: Session = Depends(get_db)
):
    tickets= (db.query(Ticket).
        filter(Ticket.customer_id == user_id).all()
    )
    
    return tickets 

# fetch all non completed pending tickets
@router.get("/all", response_model=List[TicketPublic])
def fetch_user_ticket(
    db: Session = Depends(get_db)
):
    tickets= (db.query(Ticket).
        filter(Ticket.status != "COMPLETED" and Ticket.status != "CANCELLED").all()
    )
    
    return tickets 



# fetch a tickets data [ticket data + estimate data + payment data + user data + assignment data]
@router.get("/id", response_model=List[TicketPublic])
def fetch_user_ticket(
    ticket_id: int, 
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).options(
        joinedload(Ticket.estimates),
        joinedload(Ticket.payments),
        joinedload(Ticket.assignments)
    ).filter(Ticket.id == ticket_id).all()
    
    return ticket 
