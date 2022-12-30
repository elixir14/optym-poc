import datetime
import uuid

from sqlalchemy import Column, func, TIMESTAMP, BigInteger
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, declarative_base


@as_declarative()
class CustomBase:
    id = Column(BigInteger, primary_key=True, default=uuid.uuid4)
    creation_date: datetime = Column(TIMESTAMP(timezone=True), server_default=func.now())
    update_date: datetime = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    created_by = Column(BigInteger, nullable=True)
    updated_by = Column(BigInteger, nullable=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


Base = declarative_base()
