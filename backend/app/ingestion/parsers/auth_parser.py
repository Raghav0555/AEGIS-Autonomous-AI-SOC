from app.ingestion.parsers.common import build_event
from app.schemas.event import SecurityEvent


def parse_auth_log(raw_log: dict) -> SecurityEvent:
    """
    Convert a raw authentication log into the AEGIS
    normalized SecurityEvent format.
    """

    return build_event(raw_log, source="AUTH")
