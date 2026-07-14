from __future__ import annotations

import pytest

from scripts.generate_report import (
    CHAPTER_TITLES,
    FLOW_SPECS,
    QA_ANSWERS,
    ReportInputError,
    parse_coverage_log,
    parse_pytest_log,
    parse_smoke_log,
)


def test_report_has_required_structural_content():
    assert len(CHAPTER_TITLES) == 35
    assert len(FLOW_SPECS) == 15
    assert len(QA_ANSWERS) == 22


def test_report_input_parsers_fail_closed(tmp_path):
    with pytest.raises(ReportInputError):
        parse_pytest_log(tmp_path / "missing-pytest.txt")
    failed_smoke = tmp_path / "smoke.txt"
    failed_smoke.write_text("runtime smoke: failed\n", encoding="utf-8")
    with pytest.raises(ReportInputError):
        parse_smoke_log(failed_smoke)


def test_report_input_parsers_accept_truthful_success_logs(tmp_path):
    pytest_log = tmp_path / "pytest.txt"
    pytest_log.write_text("173 passed in 1.00s\n", encoding="utf-8")
    smoke_log = tmp_path / "smoke.txt"
    smoke_log.write_text("20/20 checks passed\nSMOKE_TEST_PASSED\n", encoding="utf-8")

    assert parse_pytest_log(pytest_log).passed == 173
    assert parse_smoke_log(smoke_log).status == "passed"


def test_coverage_parser_accepts_real_module_row_format(tmp_path):
    from scripts.generate_report import CORE_MODULES

    coverage_log = tmp_path / "coverage.txt"
    rows = [f"{name:<30} 10      0   100%" for name in CORE_MODULES]
    rows.append(f"{'TOTAL':<30} 100      0   100%")
    coverage_log.write_text("\n".join(rows), encoding="utf-8")

    summary = parse_coverage_log(coverage_log)
    assert summary.total == 100
    assert all(summary.modules[name] == 100 for name in CORE_MODULES)
