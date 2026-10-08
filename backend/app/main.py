from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.incidents import router as incidents_router
from app.api.routes.health import router as health_router
from app.api.routes.events import router as events_router
from app.api.routes.incidents import router as incidents_router
from app.api.routes.detection import router as detection_router
app = FastAPI(
    title="AEGIS",
    description="Autonomous AI-powered Security Operations Center",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(
    incidents_router,
    prefix="/api",
    tags=["Incidents"],
)
app.include_router(
    detection_router,
    prefix="/api",
    tags=["Detection"],
)

@app.get("/")
def root():
    return {
        "name": "AEGIS",
        "description": "Autonomous AI-powered Security Operations Center",
        "version": "0.1.0",
    }