from typing import List
from sqlalchemy.orm import Session
from app.schemas.mechanic_assignment import MechanicAssignment
from app.models.mechanic_assignment import MechanicAssignmentModel
from app.repositories.mechanic_assignment_repository import (
    create_assignment as repo_create_assignment,
    list_assignments_by_mechanic as repo_list_assignments_by_mechanic,
)
from app.repositories.ticket_repository import update_ticket_status as repo_update_ticket_status


def assign_mechanic(db: Session, payload: MechanicAssignment) -> MechanicAssignmentModel:
    assignment = repo_create_assignment(db, payload.ticket_id, payload.mechanic_user_id)
    repo_update_ticket_status(db, payload.ticket_id, "ASSIGNED")
    return assignment


def list_assignments(db: Session, mechanic_user_id: int) -> List[MechanicAssignmentModel]:
    return repo_list_assignments_by_mechanic(db, mechanic_user_id)


