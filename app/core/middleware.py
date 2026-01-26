import logging
import time
from fastapi import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

SLOW_REQUEST_THRESHOLD_MS = 500

async def logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response | None = None
    error: Exception | None = None

    try:
        response = await call_next(request)
        return response

    except Exception as exc:
        error = exc
        raise
    
    finally:
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        
        user = getattr(request.state, "user", None)
        
        log_payload = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code if response else 500,
            "latency_ms": elapsed_ms,
            "user_id": getattr(user, "id", None),
            "role": getattr(user, "role", None),
            "authenticated": user is not None,
        }
        
        if error is not None:
            logger.error(
                "Request failed",
                extra={**log_payload, "error": str(error)},
            )
        elif elapsed_ms >= SLOW_REQUEST_THRESHOLD_MS:
            logger.warning(
                "Slow request detected",
                extra=log_payload,
            )
        else:
            logger.info(
                "Request processed",
                extra=log_payload
            )
