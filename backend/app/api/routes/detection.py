from fastapi import APIRouter, Query

from app.detection.rules.engine import detect_rules
from app.schemas.event import SecurityEvent
from app.services.event_store import load_events

router = APIRouter()


@router.get("/detection/health")
def detection_health():
    return {
        "status": "ok",
        "service": "detection-engine",
    }



@router.post("/detection/run")
def run_detection(
    severity: str | None = Query(
        default=None,
        pattern="^(low|medium|high|critical)$",
    ),
):
    events = load_events()
    alerts = []

    for event in events:
        detections = detect_rules(event)

        for detection in detections:
            alerts.append({
                "event_id": event.event_id,
                "event_type": event.event_type,
                "source": event.source,
                "user": event.user,
                "ip": event.ip,
                **detection,
            })

    if severity is not None:
        alerts = [
            alert for alert in alerts
            if alert["severity"] == severity
        ]

    return {
        "events_analyzed": len(events),
        "alerts_generated": len(alerts),
        "alerts": alerts,
    }
