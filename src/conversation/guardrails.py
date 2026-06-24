# ============================================================================
# Module: guardrails.py
# Purpose: Code-level conversation guardrails for scope and safety
# Owner: Monica Peters
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================

OFF_TOPIC_KEYWORDS = (
    "home office",
    "itemize",
    "itemized",
    "deduct",
    "deduction",
    "self-employ",
    "business",
    "llc",
    "capital gain",
    "crypto",
    "stock",
    "rental",
    "state tax",
    "efile",
    "e-file",
    "irs submit",
    "weather",
    "sports",
)


def is_off_topic(message: str) -> bool:
    """Return True when user input falls outside the v1 scope."""
    normalized = message.lower()
    return any(keyword in normalized for keyword in OFF_TOPIC_KEYWORDS)

