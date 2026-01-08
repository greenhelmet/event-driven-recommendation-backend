from fastapi import FastAPI
from app.api.v1.events import router as event_router

app = FastAPI()

app.include_router(event_router)