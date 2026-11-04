from fastapi import APIRouter, Query

from app.schemas.incident import Incident
from app.services.incident_store import load_incidents


router = APIRouter()


@router.get("/incidents", response_model=list[Incident])
def get_incidents(
    severity: str | None = Query(
        default=None,
        pattern="^(low|medium|high|critical)$",
    ),
):
    incidents = load_incidents()

    if severity is not None:
        incidents = [
            incident for incident in incidents
            if incident.severity.value == severity
        ]

    return incidents
