from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.db import get_db
from app.schemas.mechanic_assignment import MechanicAssignmentRead, MechanicAssignment
from app.services.mechanic_assignment_service import (
    assign_mechanic as svc_assign_mechanic,
    list_assignments as svc_list_assignments,
)
router =APIRouter()



@router.post("/", response_model=MechanicAssignmentRead, status_code=status.HTTP_201_CREATED)
def assign_mechanic(mechanic_assignment: MechanicAssignment, db: Session =  Depends(get_db)):
    return svc_assign_mechanic(db, mechanic_assignment)


# fetch all job assignments for a mechanic user id 
@router.get("/", response_model = List[MechanicAssignmentRead])
def fetch_assignments(
    user_id: int,
    db : Session = Depends(get_db)
):
    return svc_list_assignments(db, user_id)