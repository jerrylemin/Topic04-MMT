import importlib.util
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("generate_report", ROOT / "scripts/generate_report.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_report_wrapper_targets_the_central_two_member_generator():
    output = MODULE.generate("Lab03")
    assert output.name == "21127645_LeMinh_21127224_NguyenVuBach_Lab03_ParameterTampering.docx"
    assert output.stat().st_size > 20_000


def test_report_wrapper_does_not_create_or_update_pdf():
    source = (ROOT / "scripts/generate_report.py").read_text(encoding="utf-8").lower()
    assert "topic04_reports" in source
    assert "pdf" not in source and "soffice" not in source
