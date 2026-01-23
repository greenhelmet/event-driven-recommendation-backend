from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from enum import Enum

class EventType(str, Enum):
    click = "click"
    view = "view"
    purchase = "purchase"


class EventCreate(BaseModel):
    user_id: str = Field(..., min_length=2)
    item_id: str
    event_type: EventType
    timestamp: datetime | None = None


class EventResponse(BaseModel):
    id: int
    user_id: str
    item_id: str
    event_type: EventType
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)
