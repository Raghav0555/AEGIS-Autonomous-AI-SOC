from app.schemas.event import SecurityEvent
from app.detection.features.extractor import extract_features


def detect_rules(event: SecurityEvent) -> list[dict]:
    features = extract_features(event)

    detections = []

    # Rule 1: Brute-force pattern
    if features["failed_login_count"] > 10:
        detections.append({
            "rule": "BRUTE_FORCE",
            "severity": "high",
            "reason": (
                "More than 10 failed login attempts "
                "were detected."
            ),
        })

    # Rule 2: New privileged session
    if (
        features["new_ip"]
        and features["privilege_level"] == "admin"
    ):
        detections.append({
            "rule": "NEW_PRIVILEGED_SESSION",
            "severity": "high",
            "reason": (
                "Administrative activity originated "
                "from a previously unseen IP."
            ),
        })

    # Rule 3: Potential data exfiltration
    if (
        features["sensitive_resource_access"]
        and features["data_transfer_volume"] > 100000000
    ):
        detections.append({
            "rule": "POTENTIAL_EXFILTRATION",
            "severity": "critical",
            "reason": (
                "Sensitive resource access was followed "
                "by unusually large outbound data transfer."
            ),
        })

    return detections