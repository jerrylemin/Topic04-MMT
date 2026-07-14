from pathlib import Path

import pytest

from scripts.check_screenshots import EXPECTED_FILES, png_dimensions, validate_screenshots


def test_checker_expects_exactly_documented_thirty_six_names():
    assert len(EXPECTED_FILES) == 36
    assert EXPECTED_FILES[0] == "01_home_overview.png"
    assert EXPECTED_FILES[-1] == "36_report_files.png"
    assert len(set(EXPECTED_FILES)) == len(EXPECTED_FILES)


def test_empty_directory_reports_every_missing_screenshot(tmp_path):
    errors = validate_screenshots(tmp_path)
    assert len(errors) == 36
    assert all(error.startswith("THIẾU:") for error in errors)


def test_checker_reports_extra_file_without_content_analysis(tmp_path):
    (tmp_path / "unexpected.txt").write_text("not an image", encoding="utf-8")
    errors = validate_screenshots(tmp_path)
    assert "THỪA: unexpected.txt" in errors


def test_checker_rejects_invalid_expected_png(tmp_path):
    (tmp_path / EXPECTED_FILES[0]).write_bytes(b"not-png")
    errors = validate_screenshots(tmp_path)
    assert any(error.startswith(f"PNG KHÔNG HỢP LỆ: {EXPECTED_FILES[0]}") for error in errors)


def test_dimension_reader_rejects_non_png_file(tmp_path):
    path = tmp_path / "invalid.png"
    path.write_bytes(b"plain text")
    with pytest.raises(ValueError, match="PNG"):
        png_dimensions(path)

