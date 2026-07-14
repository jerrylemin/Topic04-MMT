from pathlib import Path

from scripts.check_screenshots import EXPECTED_FILES


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "HUONG_DAN_CHUP_ANH.md"


def test_manual_screenshot_guide_exists_and_is_substantive():
    assert GUIDE.is_file()
    assert GUIDE.stat().st_size > 10_000


def test_guide_has_one_section_for_every_expected_screenshot():
    text = GUIDE.read_text(encoding="utf-8")
    assert all(f"## {name}" in text for name in EXPECTED_FILES)
    assert len(EXPECTED_FILES) == 36


def test_each_screenshot_section_has_required_capture_fields():
    text = GUIDE.read_text(encoding="utf-8")
    required = (
        "Tên file:", "Mục đích:", "URL:", "Điều kiện ban đầu:", "Dữ liệu cần nhập:",
        "Nút cần bấm:", "Inspector cần mở:", "Timeline step cần chọn:", "Nội dung bắt buộc:",
        "Kết quả mong đợi:", "Caption báo cáo:", "Lỗi thường gặp:", "Cách làm lại:",
    )
    assert all(text.count(label) >= 36 for label in required)


def test_guide_requires_manual_capture_and_forbids_fake_images():
    text = GUIDE.read_text(encoding="utf-8").lower()
    assert "thủ công" in text
    assert "không tạo ảnh giả" in text
    assert "check_screenshots.py" in text
