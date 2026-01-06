from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.ticket import TicketCreate, TicketPublic, TicketUpdate
from app.services.ticket_service import (
    create_ticket as svc_create_ticket,
    list_user_tickets as svc_list_user_tickets,
    list_active_tickets as svc_list_active_tickets,
    get_ticket_details as svc_get_ticket_details,
    update_ticket as svc_update_ticket,
)
router = APIRouter()


@router.post(
    "/", response_model=TicketPublic, status_code=status.HTTP_201_CREATED,
    summary="Create a new ticket (job) for current user"
)
def create_ticket(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
):
    return svc_create_ticket(db, ticket_in)




# fetch user's ticket
@router.get("/", response_model=List[TicketPublic])
def fetch_user_ticket(
    user_id: int, 
    db: Session = Depends(get_db)
):
    return svc_list_user_tickets(db, user_id)

# fetch all non completed pending tickets
@router.get("/all", response_model=List[TicketPublic])
def fetch_user_ticket(
    db: Session = Depends(get_db)
):
    return svc_list_active_tickets(db)



# fetch a tickets data [ticket data + estimate data + payment data + user data + assignment data]
@router.get("/id", response_model=List[TicketPublic])
def fetch_user_ticket(
    ticket_id: int, 
    db: Session = Depends(get_db)
):
    return svc_get_ticket_details(db, ticket_id)



@router.patch(
    "/{ticket_id}", status_code=status.HTTP_201_CREATED,
    summary="Create a new ticket (job) for current user"
)
def update_ticket(
    ticket_id: int,
    ticket_in: TicketUpdate,
    db: Session = Depends(get_db),
    # current_user: AppUser = Depends(get_current_user),
):
    return svc_update_ticket(db, ticket_id, ticket_in)