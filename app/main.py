from fastapi import FastAPI
from app.schemas import Event, EventResponse

app = FastAPI()


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.get("/events/{user_id}")
def get_events(
    user_id: str,
    limit: int = 10
):
    return {"user_id": user_id, "limit": limit}


@app.post("/track", response_model=EventResponse)
def track_event(event: Event):
    return event
