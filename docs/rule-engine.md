# AEGIS Rule-Based Detection Engine

## Overview

The AEGIS rule engine performs deterministic security detection on normalized security events.

It receives a `SecurityEvent`, extracts security-relevant features, and evaluates predefined detection rules.

The output is a list of structured detections.

## Detection Flow

```text
Security Event
      ↓
Feature Extraction
      ↓
Rule Engine
      ↓
Detection Results```

## Rules

| Rule | Severity | Trigger |
|------|----------|---------|
| `BRUTE_FORCE` | high | More than 10 failed login attempts |
| `NEW_PRIVILEGED_SESSION` | high | Admin activity from a previously unseen IP |
| `POTENTIAL_EXFILTRATION` | critical | Sensitive resource access with more than 100 MB outbound transfer |

Thresholds live in `backend/app/detection/rules/constants.py`.

## API

`POST /api/detection/run` runs every rule against the stored events.

Optional query parameter `severity` (`low`, `medium`, `high`, `critical`) returns only alerts of that severity. Any other value returns `422`.
