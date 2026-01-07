from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.event import Event
from app.schemas.event import EventCreate

app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.get("/events")
def get_events(
    user_id: str,
    db: Session = Depends(get_db)
):
    return db.query(Event)\
        .filter(Event.user_id == user_id)\
        .all()


@app.post("/track")
def track_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return {"status": "ok"}
