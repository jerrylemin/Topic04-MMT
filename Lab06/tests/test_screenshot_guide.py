from pathlib import Path
from scripts.screenshot_manifest import EXPECTED_FILES
ROOT=Path(__file__).resolve().parents[1]
def test_guide_matches_nine_image_manifest():
    text=(ROOT/"HUONG_DAN_CHUP_ANH.md").read_text(encoding="utf-8")
    assert len(EXPECTED_FILES)==9 and all(name in text for name in EXPECTED_FILES)
    for label in ("Tên file:","Mục đích:","Trạng thái ban đầu:","URL hoặc lệnh:","Dữ liệu cần nhập:","Nút cần bấm:","Tab DevTools hoặc inspector cần mở:","Nội dung bắt buộc phải xuất hiện:","Kết quả đúng:","Caption dùng trong báo cáo:"):
        assert text.count(label)==9
    assert sum(line.startswith("## ") for line in text.splitlines())==4
