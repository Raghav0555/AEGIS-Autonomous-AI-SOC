from fastapi import APIRouter, Query

from app.schemas.event import SecurityEvent
from app.services.event_store import load_events


router = APIRouter()


@router.post("/events", response_model=SecurityEvent)
def ingest_event(event: SecurityEvent):
    return event


@router.get("/events", response_model=list[SecurityEvent])
def get_events(source: str | None = Query(default=None)):
    events = load_events()

    if source is not None:
        events = [
            event for event in events
            if event.source.lower() == source.lower()
        ]

    return events
