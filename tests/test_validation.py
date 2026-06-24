from src.tools.validate_w2 import (
    extract_w2_data,
    extract_w2_patch,
    parse_dependency_status,
    parse_filing_status,
)


def test_extract_full_w2_with_boxes() -> None:
    result = extract_w2_data("Box 1 40000, Box 2 2400, Box 4 40000, Box 6 40000")

    assert result.success
    assert result.data is not None
    assert result.data.box1_wages == 40000
    assert result.data.box2_federal_withheld == 2400


def test_extract_w2_defaults_box4_and_box6_for_demo() -> None:
    result = extract_w2_data("My wages are $40,000 and federal withholding is $2,400")

    assert result.success
    assert result.data is not None
    assert result.data.box4_social_security_wages == 40000
    assert result.data.box6_medicare_wages == 40000
    assert result.warnings


def test_rejects_withholding_above_wages() -> None:
    result = extract_w2_data("Box 1 40000, Box 2 50000, Box 4 40000, Box 6 40000")

    assert not result.success
    assert "cannot exceed" in result.message


def test_extract_w2_patch_updates_one_field() -> None:
    current = extract_w2_data("Box 1 40000, Box 2 2400, Box 4 40000, Box 6 40000").data
    assert current is not None

    result = extract_w2_patch("Box 2 is 2600", current)

    assert result.success
    assert result.data is not None
    assert result.data.box1_wages == 40000
    assert result.data.box2_federal_withheld == 2600


def test_parse_supported_choices() -> None:
    assert parse_filing_status("Married filing jointly") == "married_filing_jointly"
    assert parse_filing_status("single") == "single"
    assert parse_dependency_status("I am independent") is False
    assert parse_dependency_status("yes, my parents claim me") is True

