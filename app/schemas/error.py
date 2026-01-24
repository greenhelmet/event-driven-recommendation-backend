from typing import Any, Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str
    detail: Optional[Any] = None
