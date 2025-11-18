from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TicketStatus(str, Enum):
    REQUESTED = "REQUESTED"
    DISPATCH_PENDING = "DISPATCH_PENDING"
    ASSIGNED = "ASSIGNED"
    ACCEPTED = "ACCEPTED"
    ON_THE_WAY = "ON_THE_WAY"
    ESTIMATE_PROVIDED = "ESTIMATE_PROVIDED"
    ESTIMATE_APPROVED = "ESTIMATE_APPROVED"
    ESTIMATE_REJECTED = "ESTIMATE_REJECTED"
    WORK_STARTED = "WORK_STARTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TicketCreate(BaseModel):
    category: str
    vehicle_id: Optional[int] = None        # null for HOME services
    customer_location_id: int               # must belong to current user
    description: Optional[str] = Field(None, max_length=2000)


class TicketPublic(BaseModel):
    ticket_code: str
    status: TicketStatus
    service_issue_id: int
    vehicle_id: Optional[int]
    customer_location_id: Optional[int]
    description: Optional[str]

    class Config:
        from_attributes = True
