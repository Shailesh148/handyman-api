from pydantic import BaseModel, EmailStr
from typing import Optional
from typing import List

class MechanicCreate(BaseModel):
    user_id: int
    service_type_ids: List[int]
    mechanic_location_id: int

class MechanicResponse(BaseModel):
    total_jobs_completed: int
