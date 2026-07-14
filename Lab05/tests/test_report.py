from pathlib import Path
from docx import Document
from scripts import generate_report as report

def test_compact_report_contract():
    assert len(report.REPORT_SECTIONS)==9
    assert len(report.QA_ANSWERS)==5
    assert len(report.SCREENSHOTS)==8

def test_docx_has_nine_sections_and_in_place_placeholders(tmp_path:Path,monkeypatch):
    monkeypatch.setattr(report,"SHOTS",tmp_path/"screenshots")
    out=tmp_path/"report.docx";missing=report.build_docx(out);doc=Document(out)
    headings=[p.text for p in doc.paragraphs if p.style and p.style.name=="Heading 1"]
    assert headings==list(report.REPORT_SECTIONS)
    table_text="\n".join(c.text for t in doc.tables for row in t.rows for c in row.cells)
    assert len(missing)==8 and all(name in table_text for name in report.EXPECTED_FILES)
    assert "ẢNH 01/08" in table_text and "ẢNH 08/08" in table_text

def test_test_summary_never_invents_pass(tmp_path:Path):
    assert "không tuyên bố" in report._summary(tmp_path/"missing.txt","pytest")
