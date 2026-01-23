from sqlalchemy import Column, Integer, String, DateTime, Index
from datetime import datetime, timezone

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)

    user_id = Column(String, nullable=False)
    item_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)

    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    
    __table_args__ = (
        Index("idx_user_timestamp", "user_id", "timestamp"),
        Index("idx_item_timestamp", "item_id", "timestamp"),
    )
