from app.ingestion.parsers.common import build_event
from app.schemas.event import SecurityEvent


def parse_http_log(raw_log: dict) -> SecurityEvent:
    """
    Convert a raw HTTP access log into the AEGIS
    normalized SecurityEvent format.
    """

    return build_event(raw_log, source="HTTP")
