# AEGIS-Autonomous-AI-SOC
Autonomous AI-powered Security Operations Center for security event detection, correlation, investigation, and incident intelligence.
### Detection API

- `GET /api/detection/health` — checks whether the detection engine is available.
- `POST /api/detection/run` — runs the detection rules over stored events. Optional `severity` query parameter (`low`, `medium`, `high`, `critical`) filters the returned alerts.
