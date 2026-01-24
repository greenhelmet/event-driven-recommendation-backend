from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.event import EventCreate


def create_event(db: Session, event: EventCreate) -> Event:
    """
    이벤트 생성 비즈니스 로직
    """
    db_event = Event(
        user_id=event.user_id,
        item_id=event.item_id,
        event_type=event.event_type,
        event_time=event.event_time,
    )
    db.add(db_event)
    return db_event


def get_events(db: Session, skip: int, limit: int) -> list[Event]:
    return (
        db.query(Event)
        .order_by(Event.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
