from pypdf import PdfReader

from src.models.tax_data import TaxData, W2Data
from src.tools.generate_1040 import generate_1040
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


def test_generated_pdf_is_flattened_without_form_fields(tmp_path) -> None:
    values = compute_form_values(
        TaxData(
            w2=W2Data(40000, 2400, 40000, 40000),
            filing_status="single",
            is_dependent=False,
        )
    )
    path = tmp_path / "filled.pdf"
    path.write_bytes(generate_1040(values))

    reader = PdfReader(str(path))

    assert reader.get_fields() is None
    assert all("/Annots" not in page for page in reader.pages)


def test_generated_pdf_has_visible_overlay_text(tmp_path) -> None:
    values = compute_form_values(
        TaxData(
            w2=W2Data(40000, 2400, 40000, 40000),
            filing_status="single",
            is_dependent=False,
        )
    )
    path = tmp_path / "visible.pdf"
    path.write_bytes(generate_1040(values))

    text = "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)

    assert "40000" in text
    assert "15750" in text
    assert "24250" in text
    assert "2672" in text
    assert "2400" in text
    assert "272" in text
