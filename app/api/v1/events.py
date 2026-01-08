from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.event import EventCreate, EventResponse
from app.services.event_service import (
    create_event,
    get_events
)

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED
)
def create_event_api(
    event: EventCreate,
    db: Session = Depends(get_db) 
):
    return create_event(db, event)

@router.get(
    "",
    response_model=list[EventResponse],
    status_code=status.HTTP_200_OK
)
def get_events_api(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_events(db, skip, limit)