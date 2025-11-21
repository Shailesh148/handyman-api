from pydantic import BaseModel, Field
from typing import Optional, Any
from sqlalchemy import (
    Enum
)



class MechanicAssignment(BaseModel):
    mechanic_user_id: int
    ticket_id: int
    amount: int
    payment_method: str
    
class MechanicTicketRead(BaseModel):
    id: int
    ticket_code: str
    status: str
    service_issue_id: int
    vehicle_id: Optional[int]
    customer_location_id: Optional[int]
    description: Optional[str]

class MechanicAssignmentRead(BaseModel):
    id: int
    ticket_id: int
    ticket: MechanicTicketRead
    mechanic_id: int 
    status: str
    distance_km: Optional[float]
