from app.services.event_service import get_events
from app.models.event import Event
from app.schemas.event import EventType

def test_get_events_basic(db_session):
    total, events = get_events(
        db=db_session,
        skip=0,
        limit=10,
        event_type=None
    )
    
    assert isinstance(total, int)
    assert isinstance(events, list)
    
def test_get_events_filter_by_type(db_session):
    total, events = get_events(
        db=db_session,
        skip=0,
        limit=10,
        event_type=EventType.click,
    )
    
    for event in events:
        assert event.event_type == EventType.click