# AEGIS-Autonomous-AI-SOC

[![CI](https://github.com/Raghav0555/AEGIS-Autonomous-AI-SOC/actions/workflows/ci.yml/badge.svg)](https://github.com/Raghav0555/AEGIS-Autonomous-AI-SOC/actions/workflows/ci.yml)

Autonomous AI-powered Security Operations Center for security event detection, correlation, investigation, and incident intelligence.
### Events & Incidents API

- `GET /api/events` — normalized security events. Optional `source` filter (`auth`, `http`).
- `GET /api/incidents` — correlated incidents. Optional `severity` filter.

### Detection API

- `GET /api/detection/health` — checks whether the detection engine is available.
- `POST /api/detection/run` — runs the detection rules over stored events. Optional `severity` query parameter (`low`, `medium`, `high`, `critical`) filters the returned alerts.

### Running the backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run the tests with `pytest` from the `backend` directory.
