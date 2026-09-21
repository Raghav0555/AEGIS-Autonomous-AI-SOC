from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.events import router as events_router


app = FastAPI(
    title="AEGIS",
    description="Autonomous AI-powered Security Operations Center",
    version="0.1.0",
)


app.include_router(
    health_router,
    prefix="/api",
    tags=["Health"],
)

app.include_router(
    events_router,
    prefix="/api",
    tags=["Events"],
)


@app.get("/")
def root():
    return {
        "name": "AEGIS",
        "description": "Autonomous AI-powered Security Operations Center",
        "version": "0.1.0",
    }