import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.exceptions import BaseAppException
from app.schemas.error import ErrorResponse

logger = logging.getLogger(__name__)

async def app_exception_handler(
    request: Request,
    exc: BaseAppException,
):
    logger.info(
        "Application exception",
        extra={
            "code": exc.code,
            "detail": exc.detail,
            "path": request.url.path,
            "method": request.method,
        },
    )

    response = ErrorResponse(
        code=exc.code,
        message=exc.message,
        detail=exc.detail,
    )

    return JSONResponse(
        status_code=400,
        content=response.model_dump(),
    )

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    logger.info(
        "Validation error",
        extra={
            "errors": exc.errors(),
            "path": request.url.path,
        },
    )

    response = ErrorResponse(
        code="VALIDATION_ERROR",
        message="Invalid request",
        detail=exc.errors(),
    )

    return JSONResponse(
        status_code=422,
        content=response.model_dump(),
    )

async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled exception",
        extra={
            "path": request.url.path,
            "method": request.method,
        },
    )

    response = ErrorResponse(
        code="INTERNAL_SERVER_ERROR",
        message="Internal server error",
    )

    return JSONResponse(
        status_code=500,
        content=response.model_dump(),
    )
