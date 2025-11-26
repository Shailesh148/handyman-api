from pydantic import BaseModel
from typing import Dict, Any, List

class NotificationQuery(BaseModel):
    token: str
    title: str
    body: Any
    priority: str = "high" 