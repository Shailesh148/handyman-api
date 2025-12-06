from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .user import UserPublic
from .estimate import EstimatePublic
from .payment import PaymentPublic
from typing import List
from .mechanic_assignment import MechanicAssignmentRead
from .service_type import ServiceTypePublic

class TicketStatus(str, Enum):
    REQUESTED = "REQUESTED"
    DISPATCH_PENDING = "DISPATCH_PENDING"
    ASSIGNED = "ASSIGNED"
    ACCEPTED = "ACCEPTED"
    ON_THE_WAY = "ON_THE_WAY"
    ESTIMATE_PROVIDED_DELETED = "ESTIMATE_PROVIDED"
    ESTIMATE_APPROVED_DELETED = "ESTIMATE_APPROVED"
    ESTIMATE_REJECTED_DELETED = "ESTIMATE_REJECTED"
    ESTIMATE_PROVIDED = "PENDING_CUSTOMER_APPROVAL"
    ESTIMATE_APPROVED = "WORK_IN_PROGRESS"
    ESTIMATE_REJECTED = "REJECTED"
    WORK_STARTED = "WORK_STARTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TicketCreate(BaseModel):
    service: str
    vehicle_id: Optional[int] = None        # null for HOME services
    customer_location_id: Optional[int] = None               # must belong to current user
    description: Optional[str] = Field(None, max_length=2000)
    user_id: int
    photo_url: Optional[str] = None
    location_url: Optional[str] = None

class TicketUpdate(BaseModel):
    status: str
    payment_id: int

class TicketPublic(BaseModel):
    id: int
    ticket_code: str
    status: TicketStatus
    service_type: ServiceTypePublic
    vehicle_id: Optional[int]
    customer_location_id: Optional[int]
    description: Optional[str]
    customer_id: int
    customer: UserPublic
    requested_at: datetime
    preferred_payment_method: Optional[str]
    payments: List[PaymentPublic]
    estimates: List[EstimatePublic]
    assignments: List[MechanicAssignmentRead]
    photo_url: Optional[str] = None
    location_url: Optional[str] = None

    class Config:
        from_attributes = True
