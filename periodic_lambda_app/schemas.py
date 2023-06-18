from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Todo(BaseModel):
    text: str
    created: datetime = Field(default_factory=datetime.now)
    status: Literal["active", "expired", "completed"] = "active"
    inactive_since: datetime | None = None
    id: UUID = Field(default_factory=uuid4)


class TodoCreate(BaseModel):
    text: str
