from fastapi import APIRouter

from app.schemas.event import SecurityEvent


router = APIRouter()


@router.post("/events", response_model=SecurityEvent)
def ingest_event(event: SecurityEvent):
    return event