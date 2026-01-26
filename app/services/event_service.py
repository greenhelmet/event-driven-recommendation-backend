from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.event import EventCreate, EventType
from app.core.exceptions import BaseAppException
from app.core.cache import cache


def create_event(db: Session, event: EventCreate) -> Event:
    try:
        db_event = Event(
            user_id=event.user_id,
            item_id=event.item_id,
            event_type=event.event_type,
            event_time=event.event_time,
        )
        
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        
        cache.store.clear()
    
        return db_event
    
    except BaseAppException:
        db.rollback()
        raise
    
    except Exception:
        db.rollback()
        raise
        


def get_events(
    db: Session,
    skip: int,
    limit: int,
    event_type: EventType | None = None,
):
    event_type_key = event_type.value if event_type else "all"
    cache_key = f"events:type{event_type_key}:skip={skip}:limit={limit}"
    
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    
    query = db.query(Event)
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
        
    total = query.count()
    
    events = (
        query
        .order_by(Event.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    result = (total, events)
    
    cache.set(cache_key, result, ttl=60)
    
    return result