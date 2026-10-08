from fastapi import APIRouter


router = APIRouter()


@router.get("/detection/health")
def detection_health():
    return {
        "status": "ok",
        "service": "detection-engine",
    }