import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/generate_report.py"
DOCX = ROOT / "report/21127645_LeMinh_21127224_NguyenVuBach_Lab04_CSRF.docx"


def test_generator_uses_real_evidence_and_has_no_image_placeholders():
    source = SCRIPT.read_text(encoding="utf-8")
    central = (ROOT.parent / "scripts/topic04_reports.py").read_text(encoding="utf-8")
    assert "topic04_reports" in source and 'generate("Lab04")' in source
    for required in ("audit", "state", "csrf", "origin", "screenshot_manifest.py"):
        assert required in central.lower()


def test_generated_docx_and_pdf_are_real_complete_artifacts():
    result = subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=False)
    assert result.returncode == 0 and DOCX.stat().st_size > 20_000
    with zipfile.ZipFile(DOCX) as archive:
        assert archive.testzip() is None
        document = archive.read("word/document.xml")
    for text in ("21127645", "21127224", "CSRF", "Origin", "csrf_token"):
        assert text.encode("utf-8") in document
    assert "01_victim_login_session.png".encode("utf-8") in document
