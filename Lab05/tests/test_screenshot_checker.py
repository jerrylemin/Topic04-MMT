from pathlib import Path
from scripts.check_screenshots import EXPECTED_FILES,validate_screenshots,main

def test_checker_uses_eight_new_names():
    assert len(EXPECTED_FILES)==8
    assert EXPECTED_FILES[0]=="01_normal_login_search.png"
    assert EXPECTED_FILES[-1]=="08_test_report.png"

def test_empty_directory_reports_all_missing(tmp_path:Path):
    errors=validate_screenshots(tmp_path)
    assert len(errors)==8 and all(e.startswith("THIẾU:") for e in errors)

def test_extra_file_is_rejected(tmp_path:Path):
    (tmp_path/"old.png").write_bytes(b"x")
    assert "THỪA: old.png" in validate_screenshots(tmp_path)

def test_list_required_succeeds(capsys):
    assert main(["--list-required"])==0
    assert "01_normal_login_search.png" in capsys.readouterr().out
