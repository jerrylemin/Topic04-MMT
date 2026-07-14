from pathlib import Path
from scripts.check_screenshots import EXPECTED_FILES,validate_screenshots,main
def test_checker_uses_nine_new_names():
    assert len(EXPECTED_FILES)==9 and EXPECTED_FILES[0]=="01_cookie_flags.png" and EXPECTED_FILES[-1]=="09_audit_test_report.png"
def test_missing_extra_and_list_mode(tmp_path:Path,capsys):
    assert len(validate_screenshots(tmp_path))==9
    (tmp_path/"legacy.png").write_bytes(b"x")
    assert "THỪA: legacy.png" in validate_screenshots(tmp_path)
    assert main(["--list-required"])==0 and "01_cookie_flags.png" in capsys.readouterr().out
