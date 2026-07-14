from scripts.clean_submission import clean


def test_cleanup_removes_cache_directories_and_bytecode(tmp_path):
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "module.pyc").write_bytes(b"cache")
    (tmp_path / ".pytest_cache").mkdir()
    (tmp_path / "old.pyo").write_bytes(b"cache")
    removed = clean(tmp_path)
    assert "__pycache__" in removed
    assert ".pytest_cache" in removed
    assert "old.pyo" in removed
    assert not (tmp_path / "__pycache__").exists()


def test_cleanup_removes_test_database_but_preserves_demo_database(tmp_path):
    demo = tmp_path / "lab05.sqlite3"
    test_db = tmp_path / "feature_test.sqlite3"
    demo.write_bytes(b"demo")
    test_db.write_bytes(b"test")
    clean(tmp_path)
    assert demo.read_bytes() == b"demo"
    assert not test_db.exists()


def test_cleanup_preserves_source_tests_evidence_and_report(tmp_path):
    paths = [
        tmp_path / "app.py", tmp_path / "tests" / "test_app.py",
        tmp_path / "evidence" / "traces" / "trace.json", tmp_path / "report" / "report.pdf",
        tmp_path / "README.md", tmp_path / "HUONG_DAN_CHUP_ANH.md",
    ]
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("keep", encoding="utf-8")
    clean(tmp_path)
    assert all(path.read_text(encoding="utf-8") == "keep" for path in paths)


def test_cleanup_writes_real_summary_log(tmp_path):
    clean(tmp_path)
    log = tmp_path / "evidence" / "logs" / "submission_cleanup.txt"
    assert log.is_file()
    assert "LAB05 SUBMISSION CLEANUP" in log.read_text(encoding="utf-8")

