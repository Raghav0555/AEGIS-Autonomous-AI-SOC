from datetime import datetime

from app.detection.features.extractor import extract_features
from app.schemas.event import SecurityEvent


def test_security_feature_extraction():
    event = SecurityEvent(
        event_id="evt_001",
        timestamp=datetime.fromisoformat("2026-09-24T10:04:32"),
        event_type="AUTH_SUCCESS",
        source="AUTH",
        user="admin",
        ip="185.10.20.30",
        severity="medium",
        metadata={
            "failed_attempts_before": 17,
            "new_ip": True,
            "new_device": True,
            "privilege_level": "admin",
        },
    )

    features = extract_features(event)

    assert features["failed_login_count"] == 17
    assert features["new_ip"] is True
    assert features["new_device"] is True
    assert features["privilege_level"] == "admin"