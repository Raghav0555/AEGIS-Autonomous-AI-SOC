from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class EventSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SecurityEvent(BaseModel):
    event_id: str = Field(..., description="Unique identifier for the event")
    timestamp: datetime
    event_type: str
    source: str

    user: str | None = None
    ip: str | None = None

    severity: EventSeverity = EventSeverity.LOW

    metadata: dict = Field(default_factory=dict)