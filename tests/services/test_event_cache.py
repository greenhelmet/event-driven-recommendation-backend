from app.services.event_service import get_events
from app.core.cache import cache

def test_get_events_cache_hit(db_session):
    cache.store.clear()
    
    # 1차 호출 -> DB 접근
    total1, events1 = get_events(db_session, 0, 10)
    
    # 2차 호출 -> Cache hit
    total2, events2 = get_events(db_session, 0, 10)
    
    assert total1 == total2
    assert events1 == events2
    
    