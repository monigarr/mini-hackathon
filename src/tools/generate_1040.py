# ============================================================================
# Module: generate_1040.py
# Purpose: Generate a downloadable 2025 Form 1040 PDF from computed values
# Owner: Monica Peters
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

from src.models.tax_data import Form1040Values

TEMPLATE_PATH = Path("docs/1040_V2025.pdf")

TEXT_OVERLAY_COORDS = {
    "line_1a_wages": (1, 574, 333),
    "line_1z_wages_total": (1, 574, 225),
    "line_9_total_income": (1, 574, 93),
    "line_11a_agi": (1, 574, 69),
    "line_11b_agi": (2, 574, 747),
    "line_12e_standard_deduction": (2, 574, 687),
    "line_14_total_deductions": (2, 574, 651),
    "line_15_taxable_income": (2, 574, 639),
    "line_16_tax": (2, 574, 627),
    "line_24_total_tax": (2, 574, 531),
    "line_25a_w2_withholding": (2, 480, 507),
    "line_25d_total_withholding": (2, 574, 471),
    "line_33_total_payments": (2, 574, 315),
    "line_34_overpaid": (2, 574, 303),
    "line_35a_refund": (2, 574, 291),
    "line_37_amount_owed": (2, 574, 231),
}

CHECKBOX_OVERLAY_COORDS = {
    "single": (1, 40, 724),
    "married_filing_jointly": (1, 159, 724),
    "dependent_you": (2, 208, 736),
}


def _money(value: float) -> str:
    """Format a number for a narrow IRS PDF field."""
    if round(value, 2) == 0:
        return "0"
    if float(value).is_integer():
        return f"{int(value)}"
    return f"{value:.2f}"


def _visible_payload(values: Form1040Values) -> dict[str, str]:
    """Build visible overlay values keyed by semantic line ID."""
    refund = _money(values.refund) if values.refund > 0 else ""
    owed = _money(values.amount_owed) if values.amount_owed > 0 else ""
    return {
        "line_1a_wages": _money(values.wages),
        "line_1z_wages_total": _money(values.wages),
        "line_9_total_income": _money(values.total_income),
        "line_11a_agi": _money(values.adjusted_gross_income),
        "line_11b_agi": _money(values.adjusted_gross_income),
        "line_12e_standard_deduction": _money(values.standard_deduction),
        "line_14_total_deductions": _money(values.standard_deduction),
        "line_15_taxable_income": _money(values.taxable_income),
        "line_16_tax": _money(values.tax),
        "line_24_total_tax": _money(values.total_tax),
        "line_25a_w2_withholding": _money(values.federal_withholding),
        "line_25d_total_withholding": _money(values.federal_withholding),
        "line_33_total_payments": _money(values.total_payments),
        "line_34_overpaid": refund,
        "line_35a_refund": refund,
        "line_37_amount_owed": owed,
    }


def _overlay_pdf(values: Form1040Values, page_sizes: list[tuple[float, float]]) -> PdfReader:
    """Create a transparent overlay PDF with visible form values."""
    packet = BytesIO()
    pdf = canvas.Canvas(packet, pagesize=page_sizes[0])
    pdf.setTitle("Visible Form 1040 Values")

    visible_values = _visible_payload(values)
    for page_number, page_size in enumerate(page_sizes, start=1):
        pdf.setPageSize(page_size)
        pdf.setFont("Helvetica", 9)
        for key, value in visible_values.items():
            if not value:
                continue
            coord_page, x, y = TEXT_OVERLAY_COORDS[key]
            if coord_page == page_number:
                pdf.drawRightString(x, y, value)

        check_page, x, y = CHECKBOX_OVERLAY_COORDS[values.filing_status]
        if check_page == page_number:
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawCentredString(x, y, "X")
        if values.is_dependent:
            check_page, x, y = CHECKBOX_OVERLAY_COORDS["dependent_you"]
            if check_page == page_number:
                pdf.setFont("Helvetica-Bold", 9)
                pdf.drawCentredString(x, y, "X")
        pdf.showPage()

    pdf.save()
    packet.seek(0)
    return PdfReader(packet)


def _remove_form_annotations(writer: PdfWriter) -> None:
    """Flatten output by removing interactive form annotations."""
    for page in writer.pages:
        if "/Annots" in page:
            del page["/Annots"]
    if "/AcroForm" in writer._root_object:
        del writer._root_object["/AcroForm"]


def generate_1040(values: Form1040Values, template_path: Path = TEMPLATE_PATH) -> bytes:
    """Generate a completed 2025 Form 1040 PDF as bytes."""
    if not template_path.exists():
        raise FileNotFoundError(f"Missing Form 1040 template: {template_path}")

    reader = PdfReader(str(template_path))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)

    page_sizes = [
        (float(page.mediabox.width), float(page.mediabox.height))
        for page in writer.pages
    ]
    overlay = _overlay_pdf(values, page_sizes)
    for index, page in enumerate(writer.pages):
        page.merge_page(overlay.pages[index])
    _remove_form_annotations(writer)

    output = BytesIO()
    writer.write(output)
    return output.getvalue()
