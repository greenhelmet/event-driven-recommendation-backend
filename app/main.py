from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.event import router as event_router
from app.core.config import settings
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan = lifespan,
)

app.include_router(event_router)