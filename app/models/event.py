from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
