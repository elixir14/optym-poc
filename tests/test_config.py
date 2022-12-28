from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from optym_poc.core.config import settings
from optym_poc.main import app

engine = create_engine(settings.DATABASE_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)
