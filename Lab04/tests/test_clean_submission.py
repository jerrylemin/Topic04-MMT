import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _module():
    spec = importlib.util.spec_from_file_location("clean_submission", ROOT / "scripts/clean_submission.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_clean_submission_removes_cache_and_preserves_deliverables(tmp_path):
    cleaner = _module()
    cache = tmp_path / "pkg/__pycache__"
    cache.mkdir(parents=True)
    (cache / "x.pyc").write_bytes(b"cache")
    (tmp_path / ".pytest_cache").mkdir()
    report = tmp_path / "report/final.pdf"
    report.parent.mkdir()
    report.write_bytes(b"pdf")
    evidence = tmp_path / "evidence/traces/final.json"
    evidence.parent.mkdir(parents=True)
    evidence.write_text("{}", encoding="utf-8")
    demo_db = tmp_path / "lab04.sqlite3"
    demo_db.write_bytes(b"db")

    removed = cleaner.clean(tmp_path)

    assert "pkg\\__pycache__" in removed or "pkg/__pycache__" in removed
    assert report.exists() and evidence.exists() and demo_db.exists()
    assert (tmp_path / "evidence/logs/submission_cleanup.txt").exists()
