from pathlib import Path

from screenshot_manifest import (
    ALL_SCREENSHOTS,
    F12_SCREENSHOTS,
    LEGACY_SCREENSHOT_NAMES,
    OPTIONAL_SCREENSHOT_NAMES,
)


EXPECTED_FILES = tuple(item["filename"] for item in ALL_SCREENSHOTS)
DETAILED_FILES = tuple(
    name for name in LEGACY_SCREENSHOT_NAMES if name not in OPTIONAL_SCREENSHOT_NAMES
)


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "HUONG_DAN_CHUP_ANH.md"


def test_manual_screenshot_guide_exists_and_is_substantive():
    assert GUIDE.is_file()
    assert GUIDE.stat().st_size > 10_000


def test_guide_has_one_section_for_every_expected_screenshot():
    text = GUIDE.read_text(encoding="utf-8")
    assert all(name in text for name in EXPECTED_FILES)
    assert all(f"## {name}" in text for name in DETAILED_FILES)
    assert all(f"`{item['filename']}`" in text for item in F12_SCREENSHOTS)
    assert len(EXPECTED_FILES) == 50


def test_each_screenshot_section_has_required_capture_fields():
    text = GUIDE.read_text(encoding="utf-8")
    required = (
        "Tên file:", "Mục đích:", "URL:", "Điều kiện ban đầu:", "Dữ liệu cần nhập:",
        "Nút cần bấm:", "Inspector cần mở:", "Timeline step cần chọn:", "Nội dung bắt buộc:",
        "Kết quả mong đợi:", "Caption báo cáo:", "Lỗi thường gặp:", "Cách làm lại:",
    )
    assert all(text.count(label) >= len(DETAILED_FILES) for label in required)
    assert "| STT | Tên file | Mục tiêu |" in text


def test_guide_requires_manual_capture_and_forbids_fake_images():
    text = GUIDE.read_text(encoding="utf-8").lower()
    assert "thủ công" in text
    assert "không tạo ảnh giả" in text
    assert "check_screenshots.py" in text
