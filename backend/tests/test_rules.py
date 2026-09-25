from app.detection.rules.engine import detect_rules
from app.schemas.event import SecurityEvent


def test_brute_force_rule():
    event = SecurityEvent(
        event_id="evt_001",
        timestamp="2026-09-25T10:00:00",
        event_type="LOGIN_FAILURE",
        source="AUTH",
        user="admin",
        ip="185.10.20.30",
        metadata={
            "failed_attempts_before": 17,
        },
    )

    detections = detect_rules(event)

    assert len(detections) == 1
    assert detections[0]["rule"] == "BRUTE_FORCE"


def test_new_privileged_session_rule():
    event = SecurityEvent(
        event_id="evt_002",
        timestamp="2026-09-25T10:00:00",
        event_type="AUTH_SUCCESS",
        source="AUTH",
        user="admin",
        ip="185.10.20.31",
        metadata={
            "new_ip": True,
            "privilege_level": "admin",
        },
    )

    detections = detect_rules(event)

    assert detections[0]["rule"] == "NEW_PRIVILEGED_SESSION"


def test_multiple_rules():
    event = SecurityEvent(
        event_id="evt_003",
        timestamp="2026-09-25T10:00:00",
        event_type="AUTH_SUCCESS",
        source="AUTH",
        user="admin",
        ip="185.10.20.32",
        metadata={
            "failed_attempts_before": 17,
            "new_ip": True,
            "privilege_level": "admin",
            "sensitive_resource_access": True,
            "data_transfer_volume": 250000000,
        },
    )

    detections = detect_rules(event)

    rule_names = [detection["rule"] for detection in detections]

    assert "BRUTE_FORCE" in rule_names
    assert "NEW_PRIVILEGED_SESSION" in rule_names
    assert "POTENTIAL_EXFILTRATION" in rule_names