from datetime import datetime, timezone
from uuid import uuid4

from app.detection.rules.engine import detect_rules
from app.schemas.event import SecurityEvent
from app.schemas.incident import Incident, IncidentSeverity


SEVERITY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

DEFAULT_INCIDENT_TYPE = "CORRELATED_SECURITY_ACTIVITY"


def _incident_type(events: list[SecurityEvent]) -> str:
    detections = [
        detection
        for event in events
        for detection in detect_rules(event)
    ]

    if not detections:
        return DEFAULT_INCIDENT_TYPE

    most_severe = max(
        detections,
        key=lambda detection: SEVERITY_ORDER[detection["severity"]],
    )
    return most_severe["rule"]


def build_incident(events: list[SecurityEvent]) -> Incident:
    if not events:
        raise ValueError("Cannot build an incident from an empty event group")

    highest_severity = max(
        events,
        key=lambda event: SEVERITY_ORDER[event.severity.value],
    ).severity

    affected_users = sorted(
        {
            event.user
            for event in events
            if event.user is not None
        }
    )

    source_ips = sorted(
        {
            event.ip
            for event in events
            if event.ip is not None
        }
    )

    event_ids = [event.event_id for event in events]

    confidence = min(0.5 + (0.1 * (len(events) - 1)), 0.9)

    return Incident(
        incident_id=f"INC-{uuid4().hex[:8].upper()}",
        severity=IncidentSeverity(highest_severity.value),
        confidence=confidence,
        incident_type=_incident_type(events),
        affected_users=affected_users,
        source_ips=source_ips,
        events=event_ids,
        created_at=datetime.now(timezone.utc),
    )
