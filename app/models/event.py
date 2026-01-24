from sqlalchemy import Column, Integer, String, DateTime, Index
from datetime import datetime, timezone

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, nullable=False)
    item_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)

    # 이벤트 발생 시각 (client provided)
    event_time = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # 서버 생성 시각 (server responsibility)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        Index("idx_user_created_at", "user_id", "created_at"),
        Index("idx_item_created_at", "item_id", "created_at"),
    )
