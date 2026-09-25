from datetime import datetime

from app.detection.rules.engine import detect_rules
from app.schemas.event import SecurityEvent


def test_brute_force_detection():
    event = SecurityEvent(
        event_id="evt_brute_001",
        timestamp=datetime.fromisoformat(
            "2026-09-25T10:00:00"
        ),
        event_type="LOGIN_FAILURE",
        source="AUTH",
        user="admin",
        ip="185.10.20.30",
        severity="medium",
        metadata={
            "failed_attempts_before": 17,
        },
    )

    detections = detect_rules(event)

    assert len(detections) == 1
    assert detections[0]["rule"] == "BRUTE_FORCE"
    assert detections[0]["severity"] == "high"