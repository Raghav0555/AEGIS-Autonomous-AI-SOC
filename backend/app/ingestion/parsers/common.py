from datetime import datetime

from app.schemas.event import SecurityEvent


def build_event(raw_log: dict, source: str) -> SecurityEvent:
    return SecurityEvent(
        event_id=raw_log["event_id"],
        timestamp=datetime.fromisoformat(raw_log["timestamp"]),
        event_type=raw_log["event_type"],
        source=source,
        user=raw_log.get("user"),
        ip=raw_log.get("ip"),
        severity=raw_log.get("severity", "low"),
        metadata=raw_log.get("metadata", {}),
    )
