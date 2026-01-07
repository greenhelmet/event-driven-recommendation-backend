from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    click = "click"
    view = "view"
    purchase = "purchase"


class EventCreate(BaseModel):
    user_id: str = Field(..., min_length=2)
    item_id: str
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.now)


class EventResponse(BaseModel):
    user_id: str
    item_id: str
    event_type: EventType
    
    class Config:
        orm_mode = True
