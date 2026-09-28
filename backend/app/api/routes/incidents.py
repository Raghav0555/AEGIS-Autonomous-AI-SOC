from fastapi import APIRouter

from app.schemas.incident import Incident
from app.services.incident_store import load_incidents


router = APIRouter()


@router.get("/incidents", response_model=list[Incident])
def get_incidents():
    return load_incidents()