import threading
from sqlalchemy.orm import Session
from app.models.estimate import Estimate
from app.models.ticket import ESTIMATE_TO_TICKET_STATUS, Ticket
from app.models.payment import Payment
from app.schemas.estimate import EstimateUpdate, EstimateCreate
from app.repositories.estimate_repository import (
    update_estimate as repo_update_estimate,
    create_estimate as repo_create_estimate,
)
from app.repositories.payment_repository import (
    update_payment_amount as repo_update_payment_amount,
    create_payment as repo_create_payment,
)
from app.repositories.ticket_repository import update_ticket_status as repo_update_ticket_status
from app.common.messaging import send_notification


def modify_estimate(db: Session, estimate_in: EstimateUpdate) -> str:
    repo_update_estimate(db, estimate_in.id, estimate_in.status, estimate_in.amount)
    if estimate_in.status == "APPROVED":
        repo_update_payment_amount(db, estimate_in.payment_id, estimate_in.amount)
    repo_update_ticket_status(
        db, estimate_in.ticket_id, ESTIMATE_TO_TICKET_STATUS.get(estimate_in.status)
    )
    thread = threading.Thread(
        send_notification(
            "OPERATOR",
            "estimate_accepted" if estimate_in.status == "APPROVED" else "estimate_rejected",
            "https://101inc-frontend.vercel.app/en/operator/tickets",
        )
    )
    thread.start()
    return "Updated"


def create_estimate(db: Session, estimate_in: EstimateCreate) -> str:
    # Update ticket status
    repo_update_ticket_status(db, estimate_in.ticket_id, "ESTIMATE_PROVIDED")
    new_estimate = Estimate(
        ticket_id=estimate_in.ticket_id,
        mechanic_id=estimate_in.mechanic_id,
        amount=estimate_in.amount,
        status="PENDING_CUSTOMER_APPROVAL",
    )
    repo_create_estimate(db, new_estimate)
    payment = Payment(
        ticket_id=estimate_in.ticket_id,
        amount=estimate_in.amount,
        method="CASH",
        status="PENDING",
    )
    repo_create_payment(db, payment)
    thread = threading.Thread(
        send_notification(
            "CUSTOMER",
            "ticket_estimated",
            "https://101inc-frontend.vercel.app/en/my-bookings/" + str(estimate_in.ticket_id),
            estimate_in.ticket_id,
        )
    )
    thread.start()
    return "Updated"


