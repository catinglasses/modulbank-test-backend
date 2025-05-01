from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MessageCreate(BaseModel):
    sender: str
    text: str

class MessageResponse(BaseModel):
    message_id: UUID
    sender: str
    text: str
    timestamp: datetime
    serial_number: int
    user_count: int

    model_config = ConfigDict(from_attributes=True)