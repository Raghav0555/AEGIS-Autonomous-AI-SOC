from app.correlation.incident_builder import build_incident
from app.schemas.event import SecurityEvent


def create_event(
    event_id: str,
    timestamp: str,
    user: str,
    ip: str,
    severity: str,
) -> SecurityEvent:
    return SecurityEvent(
        event_id=event_id,
        timestamp=timestamp,
        event_type="AUTH_EVENT",
        source="AUTH",
        user=user,
        ip=ip,
        severity=severity,
    )


def test_builds_incident_from_correlated_events():
    events = [
        create_event(
            "evt_001",
            "2026-09-26T10:00:00",
            "admin",
            "185.10.20.30",
            "high",
        ),
        create_event(
            "evt_002",
            "2026-09-26T10:03:00",
            "admin",
            "185.10.20.30",
            "critical",
        ),
    ]

    incident = build_incident(events)

    assert incident.incident_id.startswith("INC-")
    assert incident.severity.value == "critical"
    assert incident.incident_type == "CORRELATED_SECURITY_ACTIVITY"
    assert incident.affected_users == ["admin"]
    assert incident.source_ips == ["185.10.20.30"]
    assert incident.events == ["evt_001", "evt_002"]
    assert incident.confidence == 0.6


def test_builds_incident_with_multiple_users_and_ips():
    events = [
        create_event(
            "evt_003",
            "2026-09-26T10:00:00",
            "admin",
            "185.10.20.30",
            "medium",
        ),
        create_event(
            "evt_004",
            "2026-09-26T10:02:00",
            "rahul",
            "10.0.0.15",
            "high",
        ),
    ]

    incident = build_incident(events)

    assert incident.severity.value == "high"
    assert incident.affected_users == ["admin", "rahul"]
    assert incident.source_ips == ["10.0.0.15", "185.10.20.30"]


def test_empty_events_raise_error():
    try:
        build_incident([])
        assert False
    except ValueError as error:
        assert str(error) == "Cannot build an incident from an empty event group"