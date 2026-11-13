from pydantic import BaseModel


class DetectionAlert(BaseModel):
    event_id: str
    event_type: str
    source: str
    user: str | None = None
    ip: str | None = None
    rule: str
    severity: str
    reason: str


class DetectionRunResult(BaseModel):
    events_analyzed: int
    alerts_generated: int
    alerts: list[DetectionAlert]
