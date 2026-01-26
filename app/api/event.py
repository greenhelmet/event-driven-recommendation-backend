from fastapi import APIRouter, Depends, status, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.event import EventCreate, EventResponse, EventListResponse, EventType
from app.services import event_service, event_tasks

from app.api.permissions import require_role

router = APIRouter(
    prefix="/api/v1/events",
    tags=["Events"]
)

@router.get(
    "",
    response_model=EventListResponse
)
def list_event_endpoint(
    db: Session = Depends(get_db),
    
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    
    event_type: EventType | None = Query(None),
):
    total, events = event_service.get_events(
        db=db,
        skip=skip,
        limit=limit,
        event_type=event_type,
    )
    
    return {
        "total": total,
        "items": events,
    }
    
@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))]
)
def create_event_endpoint(
    event: EventCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> EventResponse:
    db_event = event_service.create_event(db=db, event=event)
    
    # Background Tasks 등록
    background_tasks.add_task(
        event_tasks.log_event_created,
        db_event.id,
        db_event.user_id,
    )
    
    background_tasks.add_task(
        event_tasks.invalidate_event_cache
    )
        
    return EventResponse.model_validate(db_event)