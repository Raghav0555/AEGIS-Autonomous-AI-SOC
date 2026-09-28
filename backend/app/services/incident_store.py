from app.correlation.correlator import correlate_events
from app.correlation.incident_builder import build_incident
from app.schemas.incident import Incident
from app.services.event_store import load_events


def load_incidents() -> list[Incident]:
    events = load_events()
    event_groups = correlate_events(events)

    return [
        build_incident(event_group)
        for event_group in event_groups
        if event_group
    ]