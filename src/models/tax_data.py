# ============================================================================
# Module: tax_data.py
# Purpose: Data models for W-2 input, tax data, and computed Form 1040 values
# Owner: Monica Peters
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================

from dataclasses import dataclass


@dataclass(frozen=True)
class W2Data:
    """Validated W-2 fields needed for the simple Form 1040 prototype."""

    box1_wages: float
    box2_federal_withheld: float
    box4_social_security_wages: float
    box6_medicare_wages: float

    def __post_init__(self) -> None:
        """Reject impossible W-2 values early."""
        if self.box1_wages <= 0:
            raise ValueError("Box 1 wages must be positive.")
        if self.box2_federal_withheld < 0:
            raise ValueError("Box 2 federal withholding cannot be negative.")
        if self.box2_federal_withheld > self.box1_wages:
            raise ValueError("Box 2 federal withholding cannot exceed Box 1 wages.")
        if self.box4_social_security_wages <= 0:
            raise ValueError("Box 4 Social Security wages must be positive.")
        if self.box6_medicare_wages <= 0:
            raise ValueError("Box 6 Medicare wages must be positive.")


@dataclass(frozen=True)
class TaxData:
    """Collected user inputs required to compute a simple 2025 Form 1040."""

    w2: W2Data
    filing_status: str
    is_dependent: bool

    def __post_init__(self) -> None:
        """Limit v1 filing statuses to the challenge scope."""
        if self.filing_status not in {"single", "married_filing_jointly"}:
            raise ValueError("Unsupported filing status.")


@dataclass(frozen=True)
class Form1040Values:
    """Computed values that are written to Form 1040."""

    filing_status: str
    wages: float
    total_income: float
    adjusted_gross_income: float
    standard_deduction: float
    taxable_income: float
    tax: float
    total_tax: float
    federal_withholding: float
    total_payments: float
    refund: float
    amount_owed: float

