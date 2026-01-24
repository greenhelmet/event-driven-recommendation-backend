import logging
import sys
from typing import Optional


class SafeExtraFormatter(logging.Formatter):
    """
    extra 필드가 없을 때 KeyError 없이 처리하기 위한 Formatter
    """

    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, "extra"):
            record.extra = {}
        return super().format(record)


def setup_logging(log_level: str = "INFO") -> None:
    """
    애플리케이션 전역 로깅 설정

    - stdout 기반 (Docker 친화적)
    - app / uvicorn 로그 포맷 통일
    - structured logging 대응
    """

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # 기존 핸들러 제거 (pytest, uvicorn 중복 방지)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    formatter = SafeExtraFormatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s | "
            "extra=%(extra)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    # -------------------------
    # uvicorn 로그 설정
    # -------------------------
    uvicorn_loggers = [
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
    ]

    for logger_name in uvicorn_loggers:
        logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger.propagate = True
        logger.setLevel(log_level)

    # -------------------------
    # 애플리케이션 시작 로그
    # -------------------------
    logging.getLogger(__name__).info(
        "Logging initialized",
        extra={"log_level": log_level},
    )
