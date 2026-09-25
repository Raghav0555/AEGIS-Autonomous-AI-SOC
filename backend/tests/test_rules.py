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

def test_no_rules_triggered():
    event = SecurityEvent(
        event_id="evt_004",
        timestamp="2026-09-25T10:00:00",
        event_type="LOGIN_SUCCESS",
        source="AUTH",
        user="user1",
        ip="185.10.20.40",
        metadata={
            "failed_attempts_before": 2,
            "new_ip": False,
            "new_device": False,
            "privilege_level": "user",
            "sensitive_resource_access": False,
            "data_transfer_volume": 1000,
        },
    )

    detections = detect_rules(event)

    assert detections == []


def test_detection_contains_reason_and_severity():
    event = SecurityEvent(
        event_id="evt_005",
        timestamp="2026-09-25T10:00:00",
        event_type="LOGIN_FAILURE",
        source="AUTH",
        user="admin",
        ip="185.10.20.41",
        metadata={
            "failed_attempts_before": 20,
        },
    )

    detections = detect_rules(event)

    assert detections[0]["rule"] == "BRUTE_FORCE"
    assert detections[0]["severity"] == "high"
    assert "reason" in detections[0]