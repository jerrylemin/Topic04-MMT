"""Danh sách bằng chứng ảnh tối thiểu của Lab03."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent


def shot(filename, purpose, precondition, url_command, input_data, button, panel, required, expected, caption, steps):
    return {
        "filename": filename,
        "purpose": purpose,
        "precondition": precondition,
        "url_command": url_command,
        "input": input_data,
        "button": button,
        "panel": panel,
        "required": required,
        "expected": expected,
        "caption": caption,
        "steps": steps,
    }


SCREENSHOTS = [
    shot(
        "01_checkout_normal.png",
        "Chứng minh checkout bình thường dùng giá gốc.",
        "Reset database, đăng nhập user_a và thêm product 5, quantity 1 vào giỏ.",
        "http://127.0.0.1:5003/vulnerable/checkout",
        "product_id=5, quantity=1, price=100000",
        "Gửi checkout vulnerable",
        "DevTools Network > request Payload; ghép với kết quả UI.",
        "URL localhost, request POST có price=100000 và invoice/total=100000 VND.",
        "Checkout thành công với giá gốc 100000 VND.",
        "Checkout bình thường với giá sản phẩm gốc.",
        ["Mở URL checkout vulnerable.", "Giữ product_id=5, quantity=1 và price=100000.", "Bấm Gửi checkout vulnerable.", "Mở Network, chọn request POST vừa gửi.", "Chụp chung Payload và kết quả invoice 100000 VND.", "Lưu thành 01_checkout_normal.png."],
    ),
    shot(
        "02_checkout_tampered.png",
        "Chứng minh server vulnerable chấp nhận giá bị sửa.",
        "Reset database, đăng nhập user_a và thêm product 5, quantity 1.",
        "http://127.0.0.1:5003/vulnerable/checkout",
        "Sửa hidden price từ 100000 thành 1.",
        "Gửi checkout vulnerable",
        "DevTools Elements hoặc Request Inspector; ghép với invoice/Database Inspector.",
        "price=1 trong request, server dùng giá client, unit price/total=1 VND.",
        "Bản vulnerable tạo hóa đơn sai giá.",
        "Bản vulnerable tin giá do client gửi và tạo hóa đơn 1 VND.",
        ["Reset rồi mở URL checkout vulnerable.", "Sửa hidden field price=1 bằng Elements hoặc console cố định.", "Bấm Gửi checkout vulnerable.", "Mở Request hoặc Database Inspector.", "Chụp chung price=1 và invoice/total=1 VND.", "Lưu thành 02_checkout_tampered.png."],
    ),
    shot(
        "03_checkout_secure.png",
        "Chứng minh bản secure bỏ qua giá client.",
        "Reset database, đăng nhập user_a và thêm product 5, quantity 1.",
        "http://127.0.0.1:5003/secure/checkout",
        "Gửi product_id=5, quantity=1, price=1.",
        "Gửi checkout secure",
        "Request/Parameter Diff và Database hoặc Audit Inspector.",
        "Giá client=1, giá database=100000, server dùng giá database và có checkout_price_mismatch.",
        "Invoice secure có total=100000 VND; giá client không quyết định kết quả.",
        "Bản secure lấy giá từ database và ghi nhận price mismatch.",
        ["Reset rồi mở URL checkout secure.", "Nhập product_id=5, quantity=1 và thêm price=1 trong console cố định.", "Bấm Gửi checkout secure.", "Mở Parameter Diff và Database/Audit Inspector.", "Chụp vùng thấy cả client price, database price và total 100000.", "Lưu thành 03_checkout_secure.png."],
    ),
    shot(
        "04_idor_vulnerable.png",
        "Chứng minh User A xem được hóa đơn của User B.",
        "Reset database và đăng nhập user_a.",
        "http://127.0.0.1:5003/vulnerable/invoice?id=1002",
        "Đổi id từ 1001 thành 1002.",
        "GET invoice",
        "Network hoặc Request Inspector; ghép với invoice và Database Inspector.",
        "Session user_id=12, invoice 1002 owner_id=13 nhưng nội dung hóa đơn vẫn hiển thị.",
        "IDOR vulnerable thành công trong dữ liệu lab.",
        "Bản vulnerable thiếu kiểm tra ownership nên lộ invoice 1002.",
        ["Reset, đăng nhập User A và mở invoice vulnerable.", "Đổi id=1001 thành id=1002.", "Bấm GET invoice.", "Mở Request hoặc Database Inspector.", "Chụp URL, owner_id=13 và nội dung invoice 1002.", "Lưu thành 04_idor_vulnerable.png."],
    ),
    shot(
        "05_idor_secure.png",
        "Chứng minh object-level authorization chặn IDOR.",
        "Reset database và đăng nhập user_a.",
        "http://127.0.0.1:5003/secure/invoice?id=1002",
        "id=1002 khi session thuộc user_id=12.",
        "GET với authorization",
        "Authorization Inspector hoặc Network Response.",
        "HTTP 403, policy owner-or-admin=deny và không có dữ liệu dòng hàng invoice 1002.",
        "Server từ chối truy cập trái quyền trước khi render hóa đơn.",
        "Bản secure trả 403 khi User A yêu cầu invoice của User B.",
        ["Reset, đăng nhập User A và mở invoice secure.", "Nhập id=1002.", "Bấm GET với authorization.", "Mở Authorization Inspector hoặc Network Response.", "Chụp HTTP 403, decision deny và thông báo không trả dữ liệu.", "Lưu thành 05_idor_secure.png."],
    ),
    shot(
        "06_role_vulnerable.png",
        "Chứng minh mass assignment đổi role thành admin.",
        "Reset database và đăng nhập user_a.",
        "http://127.0.0.1:5003/vulnerable/profile",
        "Sửa hidden role=user thành role=admin; giữ user_id=12.",
        "Cập nhật vulnerable",
        "Elements hoặc Request Inspector; ghép với Database/Session Inspector.",
        "POST có role=admin, database trước=user sau=admin và UI/session hiển thị admin.",
        "Bản vulnerable cho phép nâng quyền trong lab.",
        "Mass assignment vulnerable chấp nhận role do client gửi.",
        ["Reset, đăng nhập User A và mở profile vulnerable.", "Sửa hidden role thành admin.", "Bấm Cập nhật vulnerable.", "Mở Request và Database/Session Inspector.", "Chụp request role=admin và kết quả role admin.", "Lưu thành 06_role_vulnerable.png."],
    ),
    shot(
        "07_role_secure.png",
        "Chứng minh secure profile bỏ qua field nhạy cảm.",
        "Reset database và đăng nhập user_a.",
        "http://127.0.0.1:5003/secure/profile",
        "Gửi email hợp lệ kèm role=admin và user_id khác qua console cố định/DevTools.",
        "Cập nhật secure",
        "Authorization, Database hoặc Audit Inspector.",
        "accepted_fields chỉ có email; role/user_id bị loại; database và session vẫn role=user.",
        "Server lấy identity từ session và giữ đúng quyền user.",
        "Bản secure dùng field allowlist và không nhận role từ client.",
        ["Reset, đăng nhập User A và mở profile secure.", "Thêm role=admin và user_id khác vào request.", "Bấm Cập nhật secure.", "Mở Authorization/Database/Audit Inspector.", "Chụp rejected_fields và role=user không đổi.", "Lưu thành 07_role_secure.png."],
    ),
    shot(
        "08_audit_test_report.png",
        "Chứng minh audit, kiểm thử và report artifacts.",
        "Đã chạy ba luồng secure; mở hai cửa sổ terminal cạnh trang audit.",
        "http://127.0.0.1:5003/audit-logs và terminal tại Lab03",
        "python -m pytest -q; python scripts/generate_report.py",
        "Filter (nếu cần), sau đó chạy hai lệnh terminal.",
        "Audit Inspector; terminal phải đọc được kết quả thật và danh sách report.",
        "Audit có checkout_price_mismatch, invoice_access_denied, sensitive_field_submitted; terminal có pytest summary thật và hai artifact report.",
        "Audit, pytest và report đều xuất hiện; không che phần tổng kết lệnh.",
        "Audit log cùng kết quả kiểm thử và report artifacts của Lab03.",
        ["Chạy các flow secure rồi mở /audit-logs.", "Chạy python -m pytest -q trong terminal.", "Chạy python scripts/generate_report.py.", "Đặt terminal cạnh Audit Inspector.", "Chụp vùng đọc được ba audit event, pytest summary và tên DOCX/PDF.", "Lưu thành 08_audit_test_report.png."],
    ),
]


def write_guide(path: Path | None = None) -> Path:
    path = path or ROOT / "HUONG_DAN_CHUP_ANH.md"
    lines = [
        "# Hướng dẫn chụp ảnh Lab03",
        "",
        "## 1. Chuẩn bị",
        "",
        "- Chỉ dùng `http://127.0.0.1:5003` và dữ liệu lab. Không dùng website thật, Playwright hoặc Selenium.",
        "- Chạy `python scripts/reset_database.py`, sau đó `python app.py`. Đăng nhập `user_a / UserA123!`.",
        "- Lưu ảnh PNG vào `evidence/screenshots/`. Có thể ghép UI với DevTools nếu mọi chữ vẫn đọc được.",
        "- Reset database và đăng nhập lại trước ảnh 01-07; ảnh 06 phải reset xong mới làm ảnh 07.",
        "",
        "## 2. Danh sách ảnh cần chụp",
        "",
    ]
    lines.extend(f"{index}. `{item['filename']}` - {item['purpose']}" for index, item in enumerate(SCREENSHOTS, 1))
    lines.extend(["", "## 3. Cách chụp từng ảnh", ""])
    fields = [
        ("Tên file", "filename"), ("Mục đích", "purpose"), ("Trạng thái ban đầu", "precondition"),
        ("URL hoặc lệnh", "url_command"), ("Dữ liệu cần nhập", "input"), ("Nút cần bấm", "button"),
        ("Tab DevTools hoặc inspector cần mở", "panel"), ("Nội dung bắt buộc phải xuất hiện", "required"),
        ("Kết quả đúng", "expected"), ("Caption dùng trong báo cáo", "caption"),
    ]
    for index, item in enumerate(SCREENSHOTS, 1):
        lines.append(f"### Ảnh {index:02d} - {item['purpose']}")
        lines.append("")
        lines.extend(f"- **{label}:** {item[key]}" for label, key in fields)
        lines.append("")
        lines.extend(f"Bước {step_index}. {step}" for step_index, step in enumerate(item["steps"], 1))
        lines.append("")
    lines.extend([
        "## 4. Cách kiểm tra và sinh báo cáo", "",
        "```powershell", "python scripts/check_screenshots.py --list-required", "python scripts/check_screenshots.py", "python scripts/generate_report.py", "```", "",
        "Nếu còn thiếu ảnh, generator vẫn tạo DOCX/PDF với khung placeholder đúng vị trí. Khi đặt đủ PNG đúng tên và hợp lệ, chạy lại generator để ảnh thật tự thay khung.", "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


if __name__ == "__main__":
    print(write_guide())
