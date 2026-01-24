from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class EventType(str, Enum):
    click = "click"
    view = "view"
    purchase = "purchase"


# =========================
# Request Schema
# =========================

class EventCreate(BaseModel):
    """
    이벤트 생성 요청 스키마
    """
    user_id: int = Field(..., gt=0)
    item_id: str = Field(..., min_length=1)
    event_type: EventType

    # 이벤트 발생 시각 (optional)
    event_time: datetime | None = None


# =========================
# Response Schema
# =========================

class EventResponse(BaseModel):
    """
    이벤트 응답 스키마 (API Contract)
    """
    id: int
    user_id: int
    item_id: str
    event_type: EventType
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
