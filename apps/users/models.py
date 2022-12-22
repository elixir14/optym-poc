from fastapi import status
from sqlalchemy import Column, String, Date, Boolean, Enum
from sqlalchemy.orm import column_property
from sqlalchemy_utils import EmailType

from apps.users.constants import Gender
from db.base import Base
from optym_poc.core.exceptions import OptymHTTPException


class User(Base):
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=True)
    email = Column(EmailType, nullable=False, unique=True)
    mobile = Column(String, nullable=False, unique=False)
    is_active = Column(Boolean, default=True)
    profile_image = Column(String, nullable=True)
    address = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    full_name = column_property(first_name + " " + last_name)

    @staticmethod
    def exist_email(db, email: str):
        data = db.query(User).filter(User.email == email).first()
        if data:
            raise OptymHTTPException(
                detail=f"Email already exist",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=-1
            )
        return True
