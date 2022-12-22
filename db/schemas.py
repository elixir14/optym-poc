import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel as PydenticBaseModel, validator


class BaseModel(PydenticBaseModel):
    class Config:
        orm_mode = True


class MobileValidatorSchema(PydenticBaseModel, ):
    mobile: str

    @validator('mobile')
    def name_must_contain_space(cls, v):
        return v.lstrip("0")


class ResponseBaseModel(BaseModel):
    id: uuid.UUID
    creation_date: Optional[datetime]
    update_date: Optional[datetime]
    created_by: Optional[uuid.UUID]
    updated_by: Optional[uuid.UUID]
    is_deleted: Optional[bool]
