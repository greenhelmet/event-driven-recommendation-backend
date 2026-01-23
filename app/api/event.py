from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.event import EventCreate, EventResponse
from app.services import event_service

router = APIRouter(
    prefix="/api/v1/events",
    tags=["Events"]
)

@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED
)
def create_event_endpoint(
    event: EventCreate,
    db: Session = Depends(get_db) 
):
    return event_service.create_event(db, event)

@router.get(
    "",
    response_model=list[EventResponse],
    status_code=status.HTTP_200_OK
)
def list_event_endpoint(
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db),
):
    return event_service.get_events(db, skip, limit)