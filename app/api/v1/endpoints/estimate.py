
from fastapi import APIRouter, status, Depends
from app.schemas.estimate import EstimatePublic, EstimateUpdate
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.estimate import Estimate
from app.models.ticket import ESTIMATE_TO_TICKET_STATUS, Ticket
from app.models.payment import Payment

router = APIRouter()


@router.post("/", response_model = str, status_code=status.HTTP_201_CREATED)
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
    return "Updated"