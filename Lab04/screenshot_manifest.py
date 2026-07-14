"""Danh sách bằng chứng ảnh tối thiểu của Lab04."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent


def shot(filename, purpose, precondition, url_command, input_data, button, panel, required, expected, caption, steps):
    return locals()


SCREENSHOTS = [
    shot("01_login_valid_request.png", "Chứng minh victim đã đăng nhập và request đổi email hợp lệ ban đầu.", "Reset database; Victim và Demo Page đang chạy; chưa đăng nhập.", "http://127.0.0.1:5004/login rồi http://127.0.0.1:5004/vulnerable/change-email", "victim / Victim123!; email=victim_initial@lab.local", "Đăng nhập; Đổi email", "DevTools Network > request POST; ghép với Dashboard.", "Session victim, POST /vulnerable/change-email và email mới trên Dashboard.", "Request cùng origin hợp lệ ban đầu đổi email thành công.", "Victim đăng nhập và gửi request đổi email hợp lệ ban đầu.", ["Mở trang login của Victim Application.", "Đăng nhập victim / Victim123! rồi mở form vulnerable.", "Nhập victim_initial@lab.local và bấm Đổi email.", "Mở Network, chọn POST /vulnerable/change-email.", "Chụp chung request và Dashboard có email mới.", "Lưu thành 01_login_valid_request.png."]),
    shot("02_csrf_demo_form.png", "Chứng minh trang Demo Page có form CSRF local cố định.", "Victim vẫn đăng nhập; mở Demo Page ở cửa sổ/tab khác.", "http://127.0.0.1:9004/attack/vulnerable-email", "Form cố định gửi email=demo_changed@lab.local đến 127.0.0.1:5004.", "Chưa gửi; chỉ mở trang", "Form Inspector hoặc DevTools Elements.", "method POST, action /vulnerable/change-email, hidden/input email cố định và cảnh báo chỉ localhost.", "Mã/giao diện form local đúng kịch bản, không có target tùy ý.", "Trang Demo Page chứa form CSRF local cố định.", ["Giữ phiên victim và mở URL Demo Page.", "Kiểm tra target/email đã cố định.", "Chưa bấm Gửi form.", "Mở Form Inspector hoặc Elements.", "Chụp form, method, action và email cùng thanh địa chỉ localhost.", "Lưu thành 02_csrf_demo_form.png."]),
    shot("03_csrf_vulnerable_changed.png", "Chứng minh CSRF vulnerable đổi email của victim.", "Victim đang đăng nhập và email chưa là demo_changed@lab.local.", "http://127.0.0.1:9004/attack/vulnerable-email", "email=demo_changed@lab.local.", "Gửi form rồi xác nhận", "DevTools Network; ghép response/trace với Dashboard Victim.", "POST được gửi, cookie/session hiện diện trong trace và email đổi thành demo_changed@lab.local.", "Route vulnerable chấp nhận request không có token và state thay đổi.", "CSRF vulnerable dùng session cookie để đổi email victim.", ["Mở Demo Page vulnerable khi victim còn đăng nhập.", "Giữ email demo_changed@lab.local.", "Bấm Gửi form và xác nhận.", "Mở Network hoặc Request Inspector của kết quả.", "Chụp request cùng Dashboard/State Inspector có email mới.", "Lưu thành 03_csrf_vulnerable_changed.png."]),
    shot("04_csrf_secure_403.png", "Chứng minh token thiếu hoặc sai bị từ chối và state không đổi.", "Reset database, đăng nhập lại victim và ghi nhớ email hiện tại.", "http://127.0.0.1:9004/attack/secure-email hoặc /attack/bad-token", "Thiếu token hoặc token sai; email=blocked@lab.local.", "Gửi form rồi xác nhận", "Network Response và CSRF/State Inspector.", "HTTP 403, token missing/invalid, database update skipped và email không đổi.", "Bản secure từ chối request trước mutation.", "CSRF token thiếu hoặc sai bị từ chối, state không đổi.", ["Reset, đăng nhập lại victim và mở Demo Page secure/bad-token.", "Giữ token thiếu/sai và email kiểm thử.", "Bấm Gửi form và xác nhận.", "Mở Network Response cùng CSRF/State Inspector.", "Chụp HTTP 403 và email trước/sau không đổi.", "Lưu thành 04_csrf_secure_403.png."]),
    shot("05_origin_blocked.png", "Chứng minh Origin/Referer validation chặn request từ Demo Page.", "Victim đã đăng nhập; dùng scenario Origin denied của Demo Page.", "http://127.0.0.1:9004/attack/secure-email", "Origin=http://127.0.0.1:9004; token không phải điều kiện quyết định ảnh này.", "Gửi form rồi xác nhận", "Origin Inspector và Network Response.", "submitted origin 9004, expected origin 5004, exact match=false, HTTP 403 và state không đổi.", "Request khác origin bị chặn trước khi cập nhật database.", "Exact Origin/Referer validation chặn request từ Demo Page.", ["Reset/đăng nhập rồi mở Demo Page secure.", "Giữ form gửi từ origin 127.0.0.1:9004.", "Bấm Gửi form và xác nhận.", "Mở Origin Inspector và Network Response.", "Chụp origin submitted/expected, deny và HTTP 403.", "Lưu thành 05_origin_blocked.png."]),
    shot("06_csrf_secure_success.png", "Chứng minh token hợp lệ cho phép request và được rotate.", "Reset database và đăng nhập victim; chỉ thao tác trên Victim Application.", "http://127.0.0.1:5004/secure/change-email", "email=secure_success@lab.local; dùng hidden token do server cấp.", "Đổi email an toàn", "CSRF Token, Origin và State Inspector.", "Origin hợp lệ, token valid, email đổi thành công và rotation status=rotated.", "Request có token/session/origin hợp lệ thành công; token cũ không còn dùng lại.", "Bản secure chấp nhận token hợp lệ và rotate token sau mutation.", ["Reset, đăng nhập và mở secure change-email trên Victim App.", "Nhập secure_success@lab.local; không sửa hidden token.", "Bấm Đổi email an toàn.", "Mở CSRF Token, Origin và State Inspector.", "Chụp valid/rotated cùng email sau cập nhật.", "Lưu thành 06_csrf_secure_success.png."]),
    shot("07_audit_test_report.png", "Chứng minh audit, kiểm thử và report artifacts.", "Đã chạy các flow vulnerable, denied và secure success.", "http://127.0.0.1:5004/audit-logs và terminal tại Lab04", "python -m pytest -q; python scripts/generate_report.py", "Filter nếu cần; chạy hai lệnh terminal", "Audit Inspector; terminal phải đọc được output thật.", "Audit có vulnerable_email_changed, csrf_token_invalid/origin denied, secure_email_changed; terminal có pytest summary và tên DOCX/PDF.", "Audit, pytest và report artifacts xuất hiện trong một ảnh đọc được.", "Audit log cùng kết quả kiểm thử và report artifacts của Lab04.", ["Mở /audit-logs sau khi chạy các flow.", "Chạy python -m pytest -q trong terminal.", "Chạy python scripts/generate_report.py.", "Đặt terminal cạnh Audit Inspector.", "Chụp vùng đọc được audit events, pytest summary và tên report.", "Lưu thành 07_audit_test_report.png."]),
]


def write_guide(path: Path | None = None) -> Path:
    path = path or ROOT / "HUONG_DAN_CHUP_ANH.md"
    lines = ["# Hướng dẫn chụp ảnh Lab04", "", "## 1. Chuẩn bị", "", "- Chỉ dùng Victim `http://127.0.0.1:5004` và Demo Page `http://127.0.0.1:9004`. Không dùng website thật hoặc browser automation.", "- Chạy `python scripts/reset_database.py`, sau đó `python run_both.py`. Tài khoản: `victim / Victim123!`.", "- Lưu PNG vào `evidence/screenshots/`. Có thể ghép UI và DevTools nếu chữ vẫn đọc được.", "- Reset database, xóa cookie cũ và đăng nhập lại trước ảnh 04-06 để state/token rõ ràng.", "", "## 2. Danh sách ảnh cần chụp", ""]
    lines.extend(f"{i}. `{x['filename']}` - {x['purpose']}" for i, x in enumerate(SCREENSHOTS, 1))
    lines += ["", "## 3. Cách chụp từng ảnh", ""]
    fields = [("Tên file", "filename"), ("Mục đích", "purpose"), ("Trạng thái ban đầu", "precondition"), ("URL hoặc lệnh", "url_command"), ("Dữ liệu cần nhập", "input_data"), ("Nút cần bấm", "button"), ("Tab DevTools hoặc inspector cần mở", "panel"), ("Nội dung bắt buộc phải xuất hiện", "required"), ("Kết quả đúng", "expected"), ("Caption dùng trong báo cáo", "caption")]
    for i, item in enumerate(SCREENSHOTS, 1):
        lines += [f"### Ảnh {i:02d} - {item['purpose']}", ""]
        lines.extend(f"- **{label}:** {item[key]}" for label, key in fields)
        lines.append("")
        lines.extend(f"Bước {n}. {step}" for n, step in enumerate(item["steps"], 1))
        lines.append("")
    lines += ["## 4. Cách kiểm tra và sinh báo cáo", "", "```powershell", "python scripts/check_screenshots.py --list-required", "python scripts/check_screenshots.py", "python scripts/generate_report.py", "```", "", "Thiếu ảnh thì DOCX/PDF vẫn có placeholder đúng vị trí. Đặt PNG hợp lệ đúng tên rồi chạy lại generator để tự thay bằng ảnh thật.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


if __name__ == "__main__":
    print(write_guide())
