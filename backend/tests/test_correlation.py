from datetime import datetime

from app.correlation.correlator import correlate_events
from app.schemas.event import SecurityEvent


def create_event(
    event_id: str,
    timestamp: str,
    user: str,
    ip: str,
) -> SecurityEvent:
    return SecurityEvent(
        event_id=event_id,
        timestamp=datetime.fromisoformat(timestamp),
        event_type="AUTH_EVENT",
        source="AUTH",
        user=user,
        ip=ip,
        severity="medium",
    )


def test_correlates_events_with_same_user_and_ip():
    events = [
        create_event(
            "evt_001",
            "2026-09-26T10:00:00",
            "admin",
            "185.10.20.30",
        ),
        create_event(
            "evt_002",
            "2026-09-26T10:03:00",
            "admin",
            "185.10.20.30",
        ),
    ]

    groups = correlate_events(events)

    assert len(groups) == 1
    assert len(groups[0]) == 2


def test_does_not_correlate_different_users():
    events = [
        create_event(
            "evt_003",
            "2026-09-26T10:00:00",
            "admin",
            "185.10.20.30",
        ),
        create_event(
            "evt_004",
            "2026-09-26T10:02:00",
            "rahul",
            "185.10.20.30",
        ),
    ]

    groups = correlate_events(events)

    assert len(groups) == 2


def test_does_not_correlate_events_outside_time_window():
    events = [
        create_event(
            "evt_005",
            "2026-09-26T10:00:00",
            "admin",
            "185.10.20.30",
        ),
        create_event(
            "evt_006",
            "2026-09-26T10:10:00",
            "admin",
            "185.10.20.30",
        ),
    ]

    groups = correlate_events(events)

    assert len(groups) == 2


def test_empty_event_list():
    groups = correlate_events([])

    assert groups == []