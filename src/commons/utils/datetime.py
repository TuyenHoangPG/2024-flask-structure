"""Helper functions for datetime, timezone and timedelta objects."""

from datetime import datetime, timezone


def utc_now():
    """Current UTC date and time with the microsecond value normalized to zero."""
    return datetime.now(timezone.utc)
