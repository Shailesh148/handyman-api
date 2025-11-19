
from fastapi import APIRouter, status, Depends
from app.schemas.mechanic_assignment import MechanicAssignmentRead, MechanicAssignment
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.estimate import Estimate
from app.models.payment import Payment
from typing import Optional
from app.models.mechanic_assignment import MechanicAssignmentModel
from app.core.db import get_db
from typing import List

router =APIRouter()



@router.post("/", response_model=MechanicAssignmentRead, status_code=status.HTTP_201_CREATED)
def assign_mechanic(mechanic_assignment: MechanicAssignment, db: Session =  Depends(get_db)):
    new_assignment =  MechanicAssignmentModel(
        ticket_id = mechanic_assignment.ticket_id,
        mechanic_id = mechanic_assignment.user_id
    )  
    
    
    db.add(new_assignment)
    db.flush()
    
    db.query(Ticket).filter(Ticket.id == mechanic_assignment.ticket_id).update(
        {"status": "ON_THE_WAY"}, synchronize_session=False
    )
    
    # create an estimate
    new_estimate = Estimate(
        ticket_id = mechanic_assignment.ticket_id,
        mechanic_id = mechanic_assignment.user_id,
        amount = mechanic_assignment.amount,
        status = "APPROVED"
    )
    
    db.add(new_estimate)
    
    # create payment
    payment = Payment(
        ticket_id = mechanic_assignment.ticket_id,
        amount = mechanic_assignment.amount,
        method = mechanic_assignment.payment_method
    )
    db.add(payment)
    
    db.commit()
    db.refresh(new_assignment)
    
    return new_assignment


# fetch all job assignments for a mechanic user id 
@router.get("/", response_model = List[MechanicAssignmentRead])
def fetch_assignments(
    user_id: int,
    db : Session = Depends(get_db)
):
    assignments = db.query(MechanicAssignmentModel).filter_by(mechanic_id=user_id).all()
    
        
    return assignments