from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.event import router as event_router
from app.core.config import settings
from app.db.init_db import init_db

from app.core.exceptions import BaseAppException
from app.core.exception_handlers import (
    app_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)
from app.core.logging import setup_logging
from app.core.middleware import logging_middleware


# =========================
# Logging Initialization
# =========================

setup_logging(settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 시작/종료 시 실행되는 라이프사이클 훅
    """
    init_db()
    yield
    # 종료 시 필요한 정리 작업이 있다면 여기 추가
    # 예: DB connection close, resource cleanup


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
    response_model_by_alias=True,
)


# =========================
# Middleware
# =========================

app.middleware("http")(logging_middleware)


# =========================
# Global Exception Handlers
# =========================

app.add_exception_handler(BaseAppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


# =========================
# Routers
# =========================

app.include_router(event_router)
