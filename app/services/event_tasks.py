import logging

logger = logging.getLogger(__name__)

def log_event_created(event_id: int, user_id: int):
    """
    이벤트 생성 후 로그 기록 (Background Task)
    """
    logger.info(
        "event_created",
        extra={
            "event_id": event_id,
            "user_id": user_id,
        },
    )
    
def invalidate_event_cache():
    """
    이벤트 관련 캐시 무효화
    """
    from app.core.cache import cache
    cache.store.clear()
    
    logger.info(
        "event_cache_invalidated",
        extra={}
    )