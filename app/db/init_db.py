import time
import logging
from sqlalchemy.exc import OperationalError

from app.db.base import Base
from app.db.session import engine
from app.models import event

logger = logging.getLogger(__name__)

def init_db(retries: int = 10, delay: int = 2) -> None:
    for i in range(retries):
        try:
            logger.info("🟢 Initializing database (attempt %d)", i + 1)
            Base.metadata.create_all(bind=engine)
            logger.info("✅ Database initialization complete")
            return
        except OperationalError as e:
            logger.warning("⚠️ DB not ready, retrying in %d seconds...", delay)
            time.sleep(delay)

    raise RuntimeError("❌ Database not available after retries")