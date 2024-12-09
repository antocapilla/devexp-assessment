from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Contact(BaseModel):
    id: str
    name: str
    phone: str

class Message(BaseModel):
    id: str
    from_: str = Field(alias="from")
    to: str
    content: str
    status: str
    created_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

class MessageDeliveryEvent(BaseModel):
    id: str
    status: str
    delivered_at: Optional[datetime] = None
    failure_reason: Optional[str] = None