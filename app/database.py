from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

logging.basicConfig(level=logging.INFO)

DATABASE_URL = "postgresql://postgres:dudwns0313@localhost:5432/test_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    logging.info("🔵 DB Session OPEN")
    try:
        yield db
    finally:
        db.close()
        logging.info("🔴 DB Session CLOSE")