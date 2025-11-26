from pydantic import BaseModel, Field
from typing import Optional


class UserDeviceCreate(BaseModel):
    user_id: int
    device_id: Optional[str] = Field(None, max_length=255)
    platform: Optional[str] = Field(None, max_length=30)
    fcm_token: str = Field(..., min_length=1)