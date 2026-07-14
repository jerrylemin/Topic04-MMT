import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/generate_report.py"
DOCX = ROOT / "report/21127645_LeMinh_Lab04_CSRF.docx"
PDF = ROOT / "report/21127645_LeMinh_Lab04_CSRF.pdf"


def test_generator_uses_real_evidence_and_has_no_image_placeholders():
    source = SCRIPT.read_text(encoding="utf-8")
    for required in ("audit_logs.json", "state_transitions.json", "pytest.txt", "coverage.txt", "runtime_smoke_test.txt", "ast.parse"):
        assert required in source
    for forbidden in ("screenshot_manifest", "01_home_overview.png", "49_report_files.png"):
        assert forbidden not in source.lower()


def test_generated_docx_and_pdf_are_real_complete_artifacts():
    assert DOCX.stat().st_size > 20_000 and PDF.stat().st_size > 10_000
    with zipfile.ZipFile(DOCX) as archive:
        assert archive.testzip() is None
        document = archive.read("word/document.xml")
    for text in (b"21127645", b"secure_email_changed", b"runtime_smoke_test.txt", b"validate_csrf_token"):
        assert text in document
    assert b"01_home_overview.png" not in document
    assert "Phụ lục B. Bằng chứng ảnh".encode("utf-8") not in document
    assert PDF.read_bytes()[:5] == b"%PDF-"
