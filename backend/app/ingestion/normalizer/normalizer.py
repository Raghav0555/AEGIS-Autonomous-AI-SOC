from app.schemas.event import SecurityEvent
from app.ingestion.parsers.auth_parser import parse_auth_log
from app.ingestion.parsers.http_parser import parse_http_log


def normalize_event(source: str, raw_log: dict) -> SecurityEvent:
    """
    Convert a raw security log into the canonical
    AEGIS SecurityEvent format.
    """

    if source == "auth":
        return parse_auth_log(raw_log)

    if source == "http":
        return parse_http_log(raw_log)

    raise ValueError(f"Unsupported event source: {source}")