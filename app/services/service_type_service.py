from sqlalchemy.orm import Session
from typing import List
from app.models.service_type import ServiceType
from app.repositories.service_type_repository import list_service_types as repo_list_service_types


def list_service_types(db: Session) -> List[ServiceType]:
    return repo_list_service_types(db)


