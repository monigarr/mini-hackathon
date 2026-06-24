# ============================================================================
# Module: validate_w2.py
# Purpose: Parse and validate W-2 fields for the simple 1040 prototype
# Owner: Monica Peters
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================

from __future__ import annotations

import re
from dataclasses import dataclass

from src.models.tax_data import W2Data

_MONEY_RE = r"\$?\s*-?\d[\d,]*(?:\.\d{1,2})?"


@dataclass(frozen=True)
class W2ValidationResult:
    """Outcome of W-2 parsing and validation."""

    success: bool
    message: str
    data: W2Data | None = None
    warnings: tuple[str, ...] = ()


def parse_money(value: str) -> float:
    """Parse a user-entered currency value into a float."""
    cleaned = value.replace("$", "").replace(",", "").strip()
    return float(cleaned)


def _find_labeled_amount(message: str, labels: tuple[str, ...]) -> float | None:
    """Find a nearby amount after one of the accepted labels."""
    for label in labels:
        pattern = rf"{label}\s*(?:is|=|:|shows|was|of|amount)?\s*({_MONEY_RE})"
        match = re.search(pattern, message, flags=re.IGNORECASE)
        if match:
            return parse_money(match.group(1))
    return None


def _fallback_amounts(message: str) -> list[float]:
    """Extract plausible money amounts when the user omits box labels."""
    values: list[float] = []
    for raw in re.findall(_MONEY_RE, message):
        try:
            value = parse_money(raw)
        except ValueError:
            continue
        if abs(value) >= 10:
            values.append(value)
    return values


def extract_w2_data(message: str) -> W2ValidationResult:
    """Extract and validate W-2 boxes 1, 2, 4, and 6 from a user message."""
    box1 = _find_labeled_amount(
        message,
        (
            r"box\s*1",
            r"wages?",
            r"w-?2\s+wages?",
            r"total\s+wages?",
        ),
    )
    box2 = _find_labeled_amount(
        message,
        (
            r"box\s*2",
            r"federal\s+(?:income\s+)?tax\s+withheld",
            r"federal\s+withholding",
            r"withheld",
        ),
    )
    box4 = _find_labeled_amount(
        message,
        (
            r"box\s*4",
            r"social\s+security\s+wages?",
            r"ss\s+wages?",
        ),
    )
    box6 = _find_labeled_amount(
        message,
        (
            r"box\s*6",
            r"medicare\s+wages?",
        ),
    )

    amounts = _fallback_amounts(message)
    if box1 is None and amounts:
        box1 = amounts[0]
    if box2 is None and len(amounts) >= 2:
        box2 = amounts[1]
    if box4 is None and len(amounts) >= 3:
        box4 = amounts[2]
    if box6 is None and len(amounts) >= 4:
        box6 = amounts[3]

    missing = []
    if box1 is None:
        missing.append("Box 1 wages")
    if box2 is None:
        missing.append("Box 2 federal tax withheld")
    if missing:
        return W2ValidationResult(
            success=False,
            message=(
                "I need the W-2 wages from Box 1 and federal tax withheld from "
                f"Box 2. Missing: {', '.join(missing)}."
            ),
        )

    warnings: list[str] = []
    if box4 is None:
        box4 = box1
        warnings.append("Box 4 was not provided, so I used Box 1 wages for this demo.")
    if box6 is None:
        box6 = box1
        warnings.append("Box 6 was not provided, so I used Box 1 wages for this demo.")

    try:
        data = W2Data(
            box1_wages=box1,
            box2_federal_withheld=box2,
            box4_social_security_wages=box4,
            box6_medicare_wages=box6,
        )
    except ValueError as exc:
        return W2ValidationResult(success=False, message=str(exc))

    if data.box1_wages < 5_000 or data.box1_wages > 150_000:
        return W2ValidationResult(
            success=False,
            message=(
                f"${data.box1_wages:,.2f} is outside the simple W-2 demo range. "
                "Use fake data for a roughly $40,000 W-2 earner."
            ),
        )

    return W2ValidationResult(
        success=True,
        message="W-2 data is valid.",
        data=data,
        warnings=tuple(warnings),
    )


def extract_w2_patch(message: str, current: W2Data) -> W2ValidationResult:
    """Apply any labeled W-2 corrections in a message to existing W-2 data."""
    box1 = _find_labeled_amount(
        message,
        (r"box\s*1", r"wages?", r"w-?2\s+wages?", r"total\s+wages?"),
    )
    box2 = _find_labeled_amount(
        message,
        (
            r"box\s*2",
            r"federal\s+(?:income\s+)?tax\s+withheld",
            r"federal\s+withholding",
            r"withheld",
        ),
    )
    box4 = _find_labeled_amount(
        message,
        (r"box\s*4", r"social\s+security\s+wages?", r"ss\s+wages?"),
    )
    box6 = _find_labeled_amount(message, (r"box\s*6", r"medicare\s+wages?"))

    if all(value is None for value in (box1, box2, box4, box6)):
        return W2ValidationResult(success=False, message="No labeled W-2 correction found.")

    try:
        data = W2Data(
            box1_wages=current.box1_wages if box1 is None else box1,
            box2_federal_withheld=current.box2_federal_withheld if box2 is None else box2,
            box4_social_security_wages=(
                current.box4_social_security_wages if box4 is None else box4
            ),
            box6_medicare_wages=current.box6_medicare_wages if box6 is None else box6,
        )
    except ValueError as exc:
        return W2ValidationResult(success=False, message=str(exc))
    return W2ValidationResult(success=True, message="W-2 correction applied.", data=data)


def parse_filing_status(message: str) -> str | None:
    """Parse supported filing status from user text."""
    normalized = message.lower()
    if "joint" in normalized or "married" in normalized or "mfj" in normalized:
        return "married_filing_jointly"
    if "single" in normalized or "unmarried" in normalized:
        return "single"
    return None


def parse_dependency_status(message: str) -> bool | None:
    """Parse whether someone can claim the user as a dependent."""
    normalized = message.lower()
    dependent_yes = (
        "yes",
        "can claim me",
        "claimed",
        "dependent",
        "parents claim",
        "parent claims",
    )
    independent_no = (
        "no",
        "cannot",
        "can't",
        "independent",
        "not a dependent",
        "nobody",
        "no one",
    )
    if any(phrase in normalized for phrase in independent_no):
        return False
    if any(phrase in normalized for phrase in dependent_yes):
        return True
    return None
