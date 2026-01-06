from typing import List
from sqlalchemy.orm import Session
from app.models.mechanic_assignment import MechanicAssignmentModel


def create_assignment(db: Session, ticket_id: int, mechanic_user_id: int) -> MechanicAssignmentModel:
    assignment = MechanicAssignmentModel(ticket_id=ticket_id, mechanic_id=mechanic_user_id)
    db.add(assignment)
    db.flush()
    db.commit()
    db.refresh(assignment)
    return assignment


def list_assignments_by_mechanic(db: Session, mechanic_user_id: int) -> List[MechanicAssignmentModel]:
    return db.query(MechanicAssignmentModel).filter_by(mechanic_id=mechanic_user_id).all()


