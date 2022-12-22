from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.pool import NullPool

from db.session import SessionLocal
from optym_poc.core.config import settings


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


def get_session():
    engine = create_engine(settings.DATABASE_URI, poolclass=NullPool)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return Session()
