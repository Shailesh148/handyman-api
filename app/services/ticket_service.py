from datetime import datetime
import threading
from typing import List
from sqlalchemy.orm import Session
from app.models.ticket import Ticket, TicketStatus, TICKET_TO_PAYMENT_STATUS
from app.models.service_type import ServiceType
from app.models.payment import Payment
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.common.messaging import send_notification
from app.repositories.ticket_repository import (
    create_ticket as repo_create_ticket,
    list_tickets_by_user as repo_list_tickets_by_user,
    list_active_tickets as repo_list_active_tickets,
    get_ticket_with_details as repo_get_ticket_with_details,
    update_ticket_status as repo_update_ticket_status,
)


def generate_ticket_code() -> str:
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"JOB-{ts}"


def create_ticket(db: Session, ticket_in: TicketCreate) -> Ticket:
    service_type = (
        db.query(ServiceType).filter(ServiceType.name == ticket_in.service).first()
    )
    ticket = Ticket(
        ticket_code=generate_ticket_code(),
        customer_id=ticket_in.user_id,
        service_type_id=service_type.id if service_type else None,
        customer_location_id=ticket_in.customer_location_id,
        status=TicketStatus.REQUESTED,
        description=ticket_in.description,
        photo_url=ticket_in.photo_url,
        location_url=ticket_in.location_url,
    )
    created = repo_create_ticket(db, ticket)
    thread = threading.Thread(
        send_notification(
            "OPERATOR",
            "ticket_created",
            "https://101inc-frontend.vercel.app/en/operator/tickets",
        )
    )
    thread.start()
    return created


def list_user_tickets(db: Session, user_id: int) -> List[Ticket]:
    return repo_list_tickets_by_user(db, user_id)


def list_active_tickets(db: Session) -> List[Ticket]:
    return repo_list_active_tickets(db)


def get_ticket_details(db: Session, ticket_id: int) -> List[Ticket]:
    return repo_get_ticket_with_details(db, ticket_id)


def update_ticket(db: Session, ticket_id: int, ticket_in: TicketUpdate) -> str:
    # Update ticket status
    repo_update_ticket_status(db, ticket_id, ticket_in.status)
    # Update payment status
    from app.repositories.payment_repository import update_payment_status

    update_payment_status(
        db, ticket_in.payment_id, TICKET_TO_PAYMENT_STATUS.get(ticket_in.status)
    )
    thread = threading.Thread(
        send_notification(
            "CUSTOMER",
            "ticket_completed",
            "https://101inc-frontend.vercel.app/en/my-bookings/" + str(ticket_id),
            ticket_id,
        )
    )
    thread.start()
    return "updated"


