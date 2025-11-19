import datetime

from pydantic import BaseModel
from pydantic.config import ConfigDict


class BaseRecordSchema(BaseModel):
    """Base schema for database records."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class BaseOutSchema(BaseRecordSchema):
    """Base output schema for database records with timestamps."""

    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


__all__ = [
    "BaseRecordSchema",
    "BaseOutSchema",
]
