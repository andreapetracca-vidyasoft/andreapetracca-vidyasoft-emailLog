from enum import Enum
from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Type(str, Enum):
    RESERVE = "RESERVE"
    RETURN = "RETURN"


class EmailDTO(BaseModel):
    email_type: Type
    send_to: str
    fields: dict
    created_at: Optional[datetime] = Field(default=None, exclude=True)


class Status(str, Enum):
    SENT = "SENT"
    FAILED = "FAILED"


class LogDTO(BaseModel):
    email_id: UUID
    status: Status
    error_message: str | None
    created_at: Optional[datetime] = None
