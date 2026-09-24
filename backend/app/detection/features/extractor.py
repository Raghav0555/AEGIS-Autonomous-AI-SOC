from app.schemas.event import SecurityEvent


def extract_features(event: SecurityEvent) -> dict:
    metadata = event.metadata

    features = {
        "failed_login_count": metadata.get("failed_attempts_before", 0),
        "request_frequency": metadata.get("request_frequency", 0.0),
        "new_ip": metadata.get("new_ip", False),
        "new_device": metadata.get("new_device", False),
        "privilege_level": metadata.get("privilege_level", "unknown"),
        "data_transfer_volume": metadata.get("data_transfer_volume", 0),
        "sensitive_resource_access": metadata.get(
            "sensitive_resource_access",
            False,
        ),
    }

    return features