import json
from pathlib import Path

from app.ingestion.normalizer.normalizer import normalize_event
from app.schemas.event import SecurityEvent


DATASET_PATH = (
    Path(__file__).resolve().parents[3]
    / "datasets"
    / "sample_events.json"
)


def load_events() -> list[SecurityEvent]:
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        raw_events = json.load(file)

    events = []

    for raw_event in raw_events:
        source = raw_event.get("source", "auth").lower()
        events.append(normalize_event(source, raw_event))

    return events