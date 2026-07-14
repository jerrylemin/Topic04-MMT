import importlib.util
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("generate_report", ROOT / "scripts/generate_report.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_report_log_cleaner_removes_ansi_and_xml_control_characters():
    assert MODULE.clean_text("\x1b[32m97 passed\x1b[0m\x00\x07") == "97 passed"


def test_report_reader_detects_powershell_utf16_log(tmp_path):
    log = tmp_path / "pytest.txt"
    log.write_text("105 passed in 1.00s", encoding="utf-16")
    assert MODULE.read_log(log) == "105 passed in 1.00s"


def test_pytest_summary_excludes_traceback(tmp_path):
    log = tmp_path / "pytest.txt"
    log.write_text(
        "Traceback line\nFileNotFoundError: missing\n"
        "FAILED tests/test_a.py::test_a\nFAILED tests/test_b.py::test_b\n",
        encoding="utf-8",
    )
    summary = MODULE.pytest_summary(log)
    assert "Traceback" not in summary and "FileNotFoundError" not in summary
    assert summary.splitlines() == ["FAILED tests/test_a.py::test_a", "FAILED tests/test_b.py::test_b"]
