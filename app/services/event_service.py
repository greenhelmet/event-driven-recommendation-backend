from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate

from sqlalchemy.exc import SQLAlchemyError


def create_event(db: Session, event: EventCreate):
    try:
        db_event = Event(**event.model_dump())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    except SQLAlchemyError:
        db.rollback()
        raise


def get_events(db: Session, skip: int, limit: int):
    return (
        db.query(Event)
        .order_by(Event.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
