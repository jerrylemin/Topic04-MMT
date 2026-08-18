from screenshot_manifest import ALL_SCREENSHOTS
from scripts.check_screenshots import check


def test_checker_expects_the_current_documented_manifest():
    names = [item["filename"] for item in ALL_SCREENSHOTS]
    assert len(names) == 50
    assert names[0] == "01_home_overview.png"
    assert names[-1] == "50_login_cookie_masked.png"
    assert len(set(names)) == len(names)


def test_empty_directory_reports_missing_screenshots(tmp_path, capsys):
    assert check(tmp_path, ALL_SCREENSHOTS) == 1
    output = capsys.readouterr().out
    assert "01_home_overview.png" in output and "Thiếu bắt buộc:" in output


def test_checker_reports_extra_file_without_content_analysis(tmp_path, capsys):
    folder = tmp_path / "evidence/screenshots"
    folder.mkdir(parents=True)
    (folder / "unexpected.txt").write_text("not an image", encoding="utf-8")
    assert check(tmp_path, ALL_SCREENSHOTS) == 1
    assert "Thừa: unexpected.txt" in capsys.readouterr().out


def test_checker_rejects_invalid_expected_png(tmp_path, capsys):
    folder = tmp_path / "evidence/screenshots"
    folder.mkdir(parents=True)
    (folder / "01_home_overview.png").write_bytes(b"not-png")
    assert check(tmp_path, ALL_SCREENSHOTS) == 1
    assert "PNG rỗng/hỏng: 01_home_overview.png" in capsys.readouterr().out

