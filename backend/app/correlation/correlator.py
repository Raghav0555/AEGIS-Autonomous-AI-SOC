from datetime import timedelta

from app.schemas.event import SecurityEvent


def correlate_events(
    events: list[SecurityEvent],
    window_minutes: int = 5,
) -> list[list[SecurityEvent]]:
    if not events:
        return []

    sorted_events = sorted(events, key=lambda event: event.timestamp)

    groups: list[list[SecurityEvent]] = []

    for event in sorted_events:
        added_to_group = False

        for group in groups:
            latest_event = group[-1]

            same_user = (
                event.user is not None
                and latest_event.user is not None
                and event.user == latest_event.user
            )

            same_ip = (
                event.ip is not None
                and latest_event.ip is not None
                and event.ip == latest_event.ip
            )

            within_window = (
                event.timestamp - latest_event.timestamp
                <= timedelta(minutes=window_minutes)
            )

            if same_user and same_ip and within_window:
                group.append(event)
                added_to_group = True
                break

        if not added_to_group:
            groups.append([event])

    return groups