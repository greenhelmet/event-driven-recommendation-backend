from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.event import EventCreate, EventResponse
from app.services import event_service
from app.core.exceptions import BaseAppException

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
    db: Session = Depends(get_db),
) -> EventResponse:
    """
    이벤트 생성 API
    (Router에서 트랜잭션 관리)
    """
    try:
        db_event = event_service.create_event(db=db, event=event)
        db.commit()
        db.refresh(db_event)
        
        return EventResponse.model_validate(db_event)

    except BaseAppException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise
