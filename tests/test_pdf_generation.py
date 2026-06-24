from pypdf import PdfReader

from src.models.tax_data import TaxData, W2Data
from src.tools.generate_1040 import FIELD_MAP, generate_1040
from src.utils.tax_tables import compute_form_values


def test_generate_1040_returns_pdf_bytes() -> None:
    values = compute_form_values(
        TaxData(
            w2=W2Data(40000, 2400, 40000, 40000),
            filing_status="single",
            is_dependent=False,
        )
    )

    pdf_bytes = generate_1040(values)

    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 1000


def test_generated_pdf_has_expected_field_values(tmp_path) -> None:
    values = compute_form_values(
        TaxData(
            w2=W2Data(40000, 2400, 40000, 40000),
            filing_status="single",
            is_dependent=False,
        )
    )
    path = tmp_path / "filled.pdf"
    path.write_bytes(generate_1040(values))

    fields = PdfReader(str(path)).get_fields()

    assert fields[FIELD_MAP["line_1a_wages"]]["/V"] == "40000"
    assert fields[FIELD_MAP["line_12e_standard_deduction"]]["/V"] == "15750"
    assert fields[FIELD_MAP["line_37_amount_owed"]]["/V"] == "272"

