from pathlib import Path

import pytest
from docx import Document
from docx.oxml.ns import qn

from scripts import generate_report as report


def test_report_contract_has_exact_chapters_questions_and_diagrams():
    assert len(report.CHAPTER_TITLES) == 30
    assert len({title for title in report.CHAPTER_TITLES}) == 30
    assert sum(len(items) for items in report.QUESTIONS_BY_CHAPTER.values()) == 15
    assert len(report.SEQUENCE_SPECS) == 4
    assert len(report.DATA_FLOW_SPECS) == 2
    assert len(report.REPORT_FLOW_KEYS) == 9


def test_required_paths_fails_closed_without_real_evidence(tmp_path: Path):
    with pytest.raises(FileNotFoundError) as error:
        report._required_paths(tmp_path)
    message = str(error.value)
    assert "audit_logs.json" in message
    assert "normal_login_vulnerable.json" in message
    assert "pytest.txt" in message
    assert "runtime_smoke_test.txt" in message


def test_log_parsers_only_report_observed_results():
    assert report._parse_pytest("================ 84 passed in 2.10s ================") == {
        "passed": 84,
        "failed": 0,
        "errors": 0,
        "status": "passed",
    }
    failed = report._parse_pytest("80 passed, 2 failed in 3.1s")
    assert failed["status"] == "failed" and failed["failed"] == 2
    coverage = report._parse_coverage("database.py 40 0 100%\nTOTAL 400 20 95%\n")
    assert coverage["rows"]["database.py"] == 100
    assert coverage["total"] == 95
    smoke = report._parse_smoke("PASS | health | HTTP 200\nPASS | login | authenticated\n")
    assert smoke["status"] == "passed" and smoke["passed_checks"] == 2
    with pytest.raises(report.EvidenceError):
        report._parse_pytest("tests were not executed")
    with pytest.raises(report.EvidenceError):
        report._parse_coverage("coverage unavailable")
    with pytest.raises(report.EvidenceError):
        report._parse_smoke("smoke not executed")


def test_table_geometry_writes_matching_grid_and_cell_widths():
    document = Document()
    table = report._add_table(document, ["Key", "Value"], [["a", "b"]], [2000, 7360])
    tbl_pr = table._tbl.tblPr
    assert tbl_pr.find(qn("w:tblW")).get(qn("w:w")) == "9360"
    assert tbl_pr.find(qn("w:tblInd")).get(qn("w:w")) == "120"
    assert tbl_pr.find(qn("w:tblLayout")).get(qn("w:type")) == "fixed"
    grid = [int(node.get(qn("w:w"))) for node in table._tbl.tblGrid]
    assert grid == [2000, 7360]
    for row in table.rows:
        assert [int(cell._tc.tcPr.tcW.get(qn("w:w"))) for cell in row.cells] == grid
    assert table.rows[0]._tr.trPr.find(qn("w:tblHeader")).get(qn("w:val")) == "true"


def test_generator_has_no_image_or_flattening_fallback_contract():
    source = Path(report.__file__).read_text(encoding="utf-8").lower()
    assert "reportlab" not in source
    assert "screenshot_manifest" not in source
    assert "01_home_overview.png" not in source
    assert "ast.parse" in source
    assert "libreoffice/soffice" in source
