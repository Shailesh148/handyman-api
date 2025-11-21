from pydantic import BaseModel, Field
from typing import Optional



class MechanicAssignment(BaseModel):
    mechanic_user_id: int
    ticket_id: int
    amount: int
    payment_method: str
    


class MechanicAssignmentRead(BaseModel):
    id: int
    ticket_id: int
    mechanic_id: int 
    status: str
    distance_km: Optional[float]
