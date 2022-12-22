from datetime import date

from apps.users.constants import Gender
from db.schemas import BaseModel


class CreateUserSchema(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    email: str
    mobile: int
    address: str
    dob: date


class UpdateUserSchema(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    mobile: int
    address: str
    dob: date
