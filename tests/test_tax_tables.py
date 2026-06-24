from src.models.tax_data import TaxData, W2Data
from src.utils.tax_tables import compute_form_values, compute_tax, standard_deduction


def test_2025_standard_deductions() -> None:
    assert standard_deduction("single", is_dependent=False, earned_income=40000) == 15750
    assert (
        standard_deduction(
            "married_filing_jointly", is_dependent=False, earned_income=40000
        )
        == 31500
    )


def test_single_filer_tax_for_40000_wages() -> None:
    assert compute_tax(24250, "single") == 2672


def test_compute_form_values_refund_or_owed() -> None:
    data = TaxData(
        w2=W2Data(40000, 2400, 40000, 40000),
        filing_status="single",
        is_dependent=False,
    )

    values = compute_form_values(data)

    assert values.standard_deduction == 15750
    assert values.taxable_income == 24250
    assert values.tax == 2672
    assert values.amount_owed == 272
    assert values.refund == 0


def test_mfj_tax_lower_for_40000_wages() -> None:
    single = compute_tax(40000 - 15750, "single")
    mfj = compute_tax(40000 - 31500, "married_filing_jointly")

    assert mfj < single

