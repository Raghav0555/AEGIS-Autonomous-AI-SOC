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
Detection Results