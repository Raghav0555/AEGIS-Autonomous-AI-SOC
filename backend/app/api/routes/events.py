from fastapi import APIRouter

from app.schemas.event import SecurityEvent
from app.services.event_store import load_events


router = APIRouter()


@router.post("/events", response_model=SecurityEvent)
def ingest_event(event: SecurityEvent):
    return event


@router.get("/events", response_model=list[SecurityEvent])
def get_events():
    return load_events()