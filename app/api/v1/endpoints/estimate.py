
from fastapi import APIRouter, status, Depends
from app.schemas.estimate import EstimatePublic, EstimateUpdate, EstimateCreate
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.estimate import Estimate
from app.models.ticket import ESTIMATE_TO_TICKET_STATUS, Ticket
from app.models.payment import Payment
import threading
from app.common.messaging import send_notification

router = APIRouter()


@router.put("/", response_model = str, status_code=status.HTTP_201_CREATED)
def modify_estimate(
    estimate_in: EstimateUpdate, 
    db: Session = Depends(get_db)
):
    # estimate update
    db.query(Estimate).filter(Estimate.id == estimate_in.id).update(
        {"status": estimate_in.status, "amount": estimate_in.amount}, synchronize_session=False
    )
    
    # update payment if estimate is approved from the customer
    if estimate_in.status == "APPROVED":
        db.query(Payment).filter(Payment.id == estimate_in.payment_id).update(
            {"amount": estimate_in.amount}, synchronize_session=False
        )
    
    # ticket status update here
    db.query(Ticket).filter(Ticket.id == estimate_in.ticket_id).update(
        {"status": ESTIMATE_TO_TICKET_STATUS.get(estimate_in.status)}, synchronize_session=False
    )
    
    db.commit()

    thread = threading.Thread(send_notification("OPERATOR", "estimate_accepted" if estimate_in.status == "APPROVED" else "estimate_rejected", "https://101inc-frontend.vercel.app/en/operator/tickets",))
    thread.start()
    
    return "Updated"


@router.post("/", response_model = str, status_code=status.HTTP_201_CREATED)
def create_estimate(
    estimate_in: EstimateCreate, 
    db: Session = Depends(get_db)
):
    db.query(Ticket).filter(Ticket.id == estimate_in.ticket_id).update(
        {"status": "ESTIMATE_PROVIDED"}, synchronize_session=False
    )
    
    # estimate create
    # create an estimate
    new_estimate = Estimate(
        ticket_id = estimate_in.ticket_id,
        mechanic_id = estimate_in.mechanic_id,
        amount = estimate_in.amount,
        status = "PENDING_CUSTOMER_APPROVAL"
    )
    
    db.add(new_estimate)
    
    # create payment
    payment = Payment(
        ticket_id = estimate_in.ticket_id,
        amount = estimate_in.amount,
        method = "CASH",
        status = "PENDING"
    )
    db.add(payment)
    
    db.commit()
    
    thread = threading.Thread(send_notification("CUSTOMER", "ticket_estimated", "https://101inc-frontend.vercel.app/en/my-bookings/" + str(estimate_in.ticket_id), estimate_in.ticket_id,))
    thread.start()
    return "Updated"