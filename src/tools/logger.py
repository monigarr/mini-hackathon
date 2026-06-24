# ============================================================================
# Module: logger.py
# Purpose: Structured JSON observation logging for agent decisions and tools
# Owner: Monica Peters
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("tax_assistant.observations")

_OBSERVATIONS: dict[str, list[dict[str, Any]]] = {}

_SENSITIVE_KEYS = {
    "ssn",
    "social_security_number",
    "ein",
    "address",
    "account",
    "routing",
    "phone",
    "email",
}


def _redact(value: Any, key: str | None = None) -> Any:
    """Return a log-safe version of user or tool data."""
    lowered = (key or "").lower()
    if any(part in lowered for part in _SENSITIVE_KEYS):
        return "[redacted]"
    if isinstance(value, str):
        cleaned = value.replace("\n", " ").strip()
        return cleaned[:180] + ("..." if len(cleaned) > 180 else "")
    if isinstance(value, dict):
        return {str(k): _redact(v, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [_redact(item) for item in value[:20]]
    return value


def log_observation(
    session_id: str,
    event_type: str,
    data: dict[str, Any] | None = None,
    *,
    state: str | None = None,
    question_count: int | None = None,
) -> dict[str, Any]:
    """Log and retain a structured observation for a session."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "event_type": event_type,
        "state": state,
        "question_count": question_count,
        "event_data": _redact(data or {}),
    }
    _OBSERVATIONS.setdefault(session_id, []).append(event)
    logger.info(json.dumps(event, sort_keys=True))
    return event


def get_observations(session_id: str) -> list[dict[str, Any]]:
    """Return observations retained for a session."""
    return list(_OBSERVATIONS.get(session_id, []))

