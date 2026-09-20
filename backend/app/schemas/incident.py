from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Incident(BaseModel):
    incident_id: str

    severity: IncidentSeverity
    confidence: float = Field(..., ge=0.0, le=1.0)

    incident_type: str

    affected_users: list[str] = Field(default_factory=list)
    source_ips: list[str] = Field(default_factory=list)

    events: list[str] = Field(default_factory=list)

    created_at: datetime