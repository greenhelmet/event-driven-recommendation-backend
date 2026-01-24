from typing import Any, Optional


class BaseAppException(Exception):
    """
    모든 비즈니스 예외의 최상위 클래스
    - HTTP 개념을 모름
    - 오직 도메인 에러 표현만 담당
    """

    def __init__(
        self,
        code: str,
        message: str,
        detail: Optional[Any] = None,
    ):
        self.code = code
        self.message = message
        self.detail = detail
        super().__init__(message)


# =========================
# Event Domain Exceptions
# =========================

class EventNotFoundException(BaseAppException):
    def __init__(self, event_id: int):
        super().__init__(
            code="EVENT_NOT_FOUND",
            message="Event not found",
            detail={"event_id": event_id},
        )


class EventAlreadyProcessedException(BaseAppException):
    def __init__(self, event_id: int):
        super().__init__(
            code="EVENT_ALREADY_PROCESSED",
            message="Event has already been processed",
            detail={"event_id": event_id},
        )


class InvalidEventStateException(BaseAppException):
    def __init__(self, event_id: int, state: str):
        super().__init__(
            code="INVALID_EVENT_STATE",
            message="Invalid event state",
            detail={
                "event_id": event_id,
                "state": state,
            },
        )
