from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    click = "click"
    view = "view"
    purchase = "purchase"


class Event(BaseModel):
    user_id: str = Field(..., min_length=2)
    item_id: str
    event_type: EventType
    timestamp: datetime


class EventResponse(BaseModel):
    user_id: str
    item_id: str
    event_type: str
