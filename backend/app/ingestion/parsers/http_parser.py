from datetime import datetime

from app.schemas.event import SecurityEvent


def parse_http_log(raw_log: dict) -> SecurityEvent:
    """
    Convert a raw HTTP access log into the AEGIS
    normalized SecurityEvent format.
    """

    return SecurityEvent(
        event_id=raw_log["event_id"],
        timestamp=datetime.fromisoformat(raw_log["timestamp"]),
        event_type=raw_log["event_type"],
        source="HTTP",
        user=raw_log.get("user"),
        ip=raw_log.get("ip"),
        severity=raw_log.get("severity", "low"),
        metadata=raw_log.get("metadata", {}),
    )