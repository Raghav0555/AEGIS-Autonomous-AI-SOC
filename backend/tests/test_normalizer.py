from app.ingestion.normalizer.normalizer import normalize_event


def test_auth_event_normalization():
    raw_event = {
        "event_id": "auth_001",
        "timestamp": "2026-09-22T10:02:11",
        "event_type": "LOGIN_FAILURE",
        "user": "admin",
        "ip": "185.10.20.30",
        "severity": "medium",
        "metadata": {
            "attempt_number": 17
        }
    }

    event = normalize_event("auth", raw_event)

    assert event.event_id == "auth_001"
    assert event.source == "AUTH"
    assert event.event_type == "LOGIN_FAILURE"
    assert event.user == "admin"
    assert event.ip == "185.10.20.30"
    assert event.severity.value == "medium"