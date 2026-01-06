from typing import List
from sqlalchemy.orm import Session, joinedload
from app.models.ticket import Ticket


def create_ticket(db: Session, ticket: Ticket) -> Ticket:
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def list_tickets_by_user(db: Session, user_id: int) -> List[Ticket]:
    return db.query(Ticket).filter(Ticket.customer_id == user_id).all()


def list_active_tickets(db: Session) -> List[Ticket]:
    # Avoid Python 'and' on column objects; use != on enum/status where clause will be optimized later
    return db.query(Ticket).filter(Ticket.status.notin_(["COMPLETED", "CANCELLED"])).all()


def get_ticket_with_details(db: Session, ticket_id: int) -> List[Ticket]:
    return (
        db.query(Ticket)
        .options(
            joinedload(Ticket.estimates),
            joinedload(Ticket.payments),
            joinedload(Ticket.assignments),
        )
        .filter(Ticket.id == ticket_id)
        .all()
    )


def update_ticket_status(db: Session, ticket_id: int, status_value: str) -> None:
    from app.models.ticket import Ticket as TicketModel

    db.query(TicketModel).filter(TicketModel.id == ticket_id).update(
        {"status": status_value}, synchronize_session=False
    )
    db.commit()


def delete_tickets_by_customer_id(db: Session, user_id: int) -> None:
    db.query(Ticket).filter(Ticket.customer_id == user_id).delete(synchronize_session=False)


