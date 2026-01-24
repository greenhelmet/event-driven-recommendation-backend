import logging
from typing import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    logger.debug("DB Session OPEN")
    
    try:
        yield db
    finally:
        db.close()
        logger.debug("DB Session CLOSE")
