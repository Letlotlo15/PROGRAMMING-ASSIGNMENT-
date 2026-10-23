from datetime import datetime, timedelta

CAMPUS_POLICIES = {
    "Johannesburg": {
        "max_duration_minutes": 120,
        "open_hour": 7,
        "close_hour": 18,
        "description": "Max 2 hours, 07:00-18:00",
    },
    "Cape Town": {
        "max_duration_minutes": 240,
        "open_hour": 8,
        "close_hour": 21,
        "description": "Max 4 hours, 08:00-21:00 (extended)",
    },
    "Durban": {
        "max_duration_minutes": 90,
        "open_hour": 8,
        "close_hour": 16,
        "description": "Max 90 minutes, 08:00-16:00",
    },
}


def get_policy(campus):
    return CAMPUS_POLICIES.get(campus)


def validate_booking(campus, start_time, duration_minutes):
    policy = get_policy(campus)
    if not policy:
        return False, f"Unknown campus: {campus}"

    if duration_minutes <= 0:
        return False, "Duration must be positive."
    if duration_minutes > policy["max_duration_minutes"]:
        return False, (f"{campus} allows a maximum of "
                       f"{policy['max_duration_minutes']} minutes.")

    try:
        start = datetime.strptime(start_time, "%H:%M")
    except ValueError:
        return False, "Start time must be in HH:MM format."

    end = start + timedelta(minutes=duration_minutes)
    if start.hour < policy["open_hour"]:
        return False, f"{campus} opens at {policy['open_hour']:02d}:00."
    if end.hour > policy["close_hour"] or (end.hour == policy["close_hour"] and end.minute > 0):
        return False, f"{campus} closes at {policy['close_hour']:02d}:00."

    return True, f"OK — {campus} policy: {policy['description']}"