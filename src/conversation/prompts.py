# ============================================================================
# Module: prompts.py
# Purpose: Deterministic, warm user-facing copy for the chat flow
# Owner: Monica Peters
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================

from src.models.tax_data import W2Data
from src.utils.tax_tables import FILING_STATUS_LABELS

DISCLAIMER = (
    "Prototype only: this is for fake W-2 demo data, not tax advice, not "
    "e-filing, and not a professional tax preparation service."
)


def ask_w2() -> str:
    """Return the first question asking for W-2 data."""
    return (
        ""
        f"{DISCLAIMER}\n\n"
        "Question 1 of 5: A) Your Wages B) Your Federal Tax "
        "withheld. Optional: C) Your Social Security Wages D) "
        "Your Medicare Wages. Example: A) 40000, B) 2400, "
        "C) 40000, D) 40000"
    )


def ask_filing_status(w2: W2Data) -> str:
    """Return the filing status question."""
    return (
        f"Thanks. I have wages of ${w2.box1_wages:,.2f} and federal withholding "
        f"of ${w2.box2_federal_withheld:,.2f}.\n\n"
        "Question 2 of 5: are you filing as Single or Married Filing Jointly?"
    )


def ask_dependency() -> str:
    """Return the dependency question."""
    return (
        "Question 3 of 5: can someone else claim you as a dependent, "
        "or are you independent for this return?"
    )


def ask_confirmation(w2: W2Data, filing_status: str, is_dependent: bool) -> str:
    """Return the confirmation question."""
    dependent_text = "someone can claim you as a dependent" if is_dependent else "you are independent"
    return (
        "Question 4 of 5: just to confirm before I generate the form:\n"
        f"- A) Your Wages: ${w2.box1_wages:,.2f}\n"
        f"- B) Your Federal Tax Withheld: ${w2.box2_federal_withheld:,.2f}\n"
        f"- C)Filing status: {FILING_STATUS_LABELS[filing_status]}\n"
        f"- D) Dependency: {dependent_text}\n\n"
        "Is that correct?"
    )


def ask_correction() -> str:
    """Return the fifth and final question when the user rejects confirmation."""
    return (
        "Question 5 of 5: tell me the one thing to correct now. "
        "For example: 'Box 2 is 2600', 'Single', or 'I am independent'."
    )


def off_topic_redirect() -> str:
    """Return a scoped redirect for off-topic or advice-seeking messages."""
    return (
        "That’s outside this prototype's scope. I can only collect fake W-2 "
        "data for a simple 2025 Form 1040 and generate a downloadable draft. "
        "For tax advice or complex situations, use a qualified tax professional. "
        "Let's stay with the current question."
    )

