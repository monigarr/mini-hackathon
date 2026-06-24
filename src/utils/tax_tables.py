# ============================================================================
# Module: tax_tables.py
# Purpose: Compute 2025 federal tax values for simple W-2 Form 1040 filings
# Owner: Monica Peters
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================

from src.models.tax_data import Form1040Values, TaxData

FILING_STATUS_LABELS = {
    "single": "Single",
    "married_filing_jointly": "Married Filing Jointly",
}

STANDARD_DEDUCTION_2025 = {
    "single": 15_750.0,
    "married_filing_jointly": 31_500.0,
}

DEPENDENT_MINIMUM_STANDARD_DEDUCTION_2025 = 1_350.0
DEPENDENT_EARNED_INCOME_ADDITION_2025 = 450.0

TAX_BRACKETS_2025 = {
    "single": [
        (11_925.0, 0.10),
        (48_475.0, 0.12),
        (103_350.0, 0.22),
        (197_300.0, 0.24),
        (250_525.0, 0.32),
        (626_350.0, 0.35),
        (float("inf"), 0.37),
    ],
    "married_filing_jointly": [
        (23_850.0, 0.10),
        (96_950.0, 0.12),
        (206_700.0, 0.22),
        (394_600.0, 0.24),
        (501_050.0, 0.32),
        (751_600.0, 0.35),
        (float("inf"), 0.37),
    ],
}


def standard_deduction(
    filing_status: str,
    *,
    is_dependent: bool,
    earned_income: float,
) -> float:
    """Return the 2025 standard deduction for the supported filing status."""
    regular = STANDARD_DEDUCTION_2025[filing_status]
    if not is_dependent:
        return regular
    dependent_amount = max(
        DEPENDENT_MINIMUM_STANDARD_DEDUCTION_2025,
        earned_income + DEPENDENT_EARNED_INCOME_ADDITION_2025,
    )
    return min(regular, dependent_amount)


def compute_tax(taxable_income: float, filing_status: str) -> float:
    """Compute federal tax using 2025 marginal brackets."""
    remaining = max(0.0, taxable_income)
    lower = 0.0
    tax = 0.0
    for upper, rate in TAX_BRACKETS_2025[filing_status]:
        if remaining <= 0:
            break
        taxable_at_rate = min(remaining, upper - lower)
        tax += taxable_at_rate * rate
        remaining -= taxable_at_rate
        lower = upper
    return round(tax)


def compute_form_values(tax_data: TaxData) -> Form1040Values:
    """Compute the in-scope Form 1040 line values from validated tax data."""
    wages = round(tax_data.w2.box1_wages, 2)
    deduction = standard_deduction(
        tax_data.filing_status,
        is_dependent=tax_data.is_dependent,
        earned_income=wages,
    )
    taxable_income = max(0.0, wages - deduction)
    tax = compute_tax(taxable_income, tax_data.filing_status)
    withholding = round(tax_data.w2.box2_federal_withheld, 2)
    refund = max(0.0, withholding - tax)
    amount_owed = max(0.0, tax - withholding)
    return Form1040Values(
        filing_status=tax_data.filing_status,
        is_dependent=tax_data.is_dependent,
        wages=wages,
        total_income=wages,
        adjusted_gross_income=wages,
        standard_deduction=deduction,
        taxable_income=round(taxable_income, 2),
        tax=tax,
        total_tax=tax,
        federal_withholding=withholding,
        total_payments=withholding,
        refund=round(refund, 2),
        amount_owed=round(amount_owed, 2),
    )
